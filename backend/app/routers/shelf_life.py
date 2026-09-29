import json
from datetime import datetime, date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.models.inventory import Inventory
from app.models.analysis import AnalysisResult
from app.models.storage import StorageCondition
from app.models.shelf_life import ShelfLifePrediction
from app.schemas.shelf_life import ShelfLifePredictionRequest, ShelfLifePredictionResponse
from app.core.security import get_current_active_user
from app.ml import run_shelf_life_prediction

router = APIRouter(prefix="/api/shelf-life", tags=["Predictive Shelf-Life Monitoring"])

def prepare_shelf_life_response(record: ShelfLifePrediction) -> ShelfLifePredictionResponse:
    storage_impact_val = json.loads(record.storage_impact) if isinstance(record.storage_impact, str) else record.storage_impact
    contributing_factors_val = json.loads(record.contributing_factors) if isinstance(record.contributing_factors, str) else record.contributing_factors
    storage_guidance_val = json.loads(record.storage_guidance) if isinstance(record.storage_guidance, str) else record.storage_guidance
    input_features_val = json.loads(record.input_features) if isinstance(record.input_features, str) else record.input_features

    has_image_analysis = input_features_val.get("has_image_analysis", record.analysis_id is not None)
    has_storage_log = input_features_val.get("has_storage_log", False)
    degradation_rate_per_day = input_features_val.get("degradation_rate_per_day")
    sufficient_data = input_features_val.get("sufficient_data", False)

    return ShelfLifePredictionResponse(
        id=record.id,
        inventory_id=record.inventory_id,
        analysis_id=record.analysis_id,
        user_id=record.user_id,
        estimated_remaining_days=record.estimated_remaining_days,
        estimated_expiry_date=record.estimated_expiry_date,
        risk_level=record.risk_level,
        confidence=record.confidence,
        trend=record.trend,
        has_image_analysis=has_image_analysis,
        has_storage_log=has_storage_log,
        degradation_rate_per_day=degradation_rate_per_day,
        sufficient_data=sufficient_data,
        storage_impact=storage_impact_val,
        contributing_factors=contributing_factors_val,
        storage_guidance=storage_guidance_val,
        input_features=input_features_val,
        model_version=record.model_version,
        created_at=record.created_at
    )

@router.post("/predict", response_model=ShelfLifePredictionResponse, status_code=status.HTTP_201_CREATED)
def generate_shelf_life_prediction(
    data: ShelfLifePredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    inv = db.query(Inventory).filter(Inventory.id == data.inventory_id).first()
    if not inv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory batch #{data.inventory_id} not found."
        )

    # 1. Fetch image analysis for this inventory batch
    analysis = None
    if data.analysis_id:
        analysis = db.query(AnalysisResult).filter(AnalysisResult.id == data.analysis_id).first()
    else:
        analysis = db.query(AnalysisResult).filter(
            AnalysisResult.inventory_id == data.inventory_id
        ).order_by(AnalysisResult.created_at.desc()).first()

    # Explicit image analysis identification (no silent fallbacks pretending image analysis exists)
    has_image_analysis = analysis is not None
    freshness_score = analysis.freshness_score if analysis else 100
    freshness_category = analysis.predicted_category if analysis else "Good"
    spoilage_prob = analysis.spoilage_probability if analysis else 0.0

    # 2. Fetch latest storage condition record
    latest_storage = db.query(StorageCondition).filter(
        StorageCondition.inventory_id == data.inventory_id
    ).order_by(StorageCondition.created_at.desc()).first()

    has_storage_log = latest_storage is not None

    storage_temp = data.temperature_override if data.temperature_override is not None else (
        latest_storage.temperature if latest_storage else inv.storage_temperature
    )
    storage_hum = data.humidity_override if data.humidity_override is not None else (
        latest_storage.humidity if latest_storage else inv.storage_humidity
    )
    storage_cond = data.storage_condition_override if data.storage_condition_override is not None else (
        latest_storage.storage_condition if latest_storage else "Refrigerated"
    )
    packaging = data.packaging_type_override if data.packaging_type_override is not None else (
        latest_storage.packaging_type if latest_storage else inv.packaging_type
    )
    duration_days = latest_storage.storage_duration_days if latest_storage else inv.storage_duration

    # 3. Fetch past image analyses for timestamp-based degradation velocity
    past_analyses = db.query(AnalysisResult).filter(
        AnalysisResult.inventory_id == data.inventory_id
    ).order_by(AnalysisResult.created_at.asc()).all()

    past_records = [
        {
            "freshness_score": a.freshness_score,
            "created_at": a.created_at
        }
        for a in past_analyses
    ]

    # 4. Execute Predictive Model Engine
    food_category = inv.food_item.category if inv.food_item else "Fruits"
    prediction_dict = run_shelf_life_prediction(
        food_category=food_category,
        freshness_score=freshness_score,
        freshness_category=freshness_category,
        spoilage_probability=spoilage_prob,
        has_image_analysis=has_image_analysis,
        has_storage_log=has_storage_log,
        purchase_date=inv.purchase_date,
        storage_temperature=storage_temp,
        storage_humidity=storage_hum,
        packaging_type=packaging,
        storage_condition=storage_cond,
        storage_duration_days=duration_days,
        past_analysis_records=past_records
    )

    expiry_date_val = datetime.strptime(prediction_dict["estimated_expiry_date"], "%Y-%m-%d").date()

    # 5. Persist Prediction Result
    prediction_record = ShelfLifePrediction(
        inventory_id=data.inventory_id,
        analysis_id=analysis.id if analysis else None,
        user_id=current_user.id,
        estimated_remaining_days=prediction_dict["estimated_remaining_days"],
        estimated_expiry_date=expiry_date_val,
        risk_level=prediction_dict["risk_level"],
        confidence=prediction_dict["confidence"],
        trend=prediction_dict["trend"],
        storage_impact=json.dumps(prediction_dict["storage_impact"]),
        contributing_factors=json.dumps(prediction_dict["contributing_factors"]),
        storage_guidance=json.dumps(prediction_dict["storage_guidance"]),
        input_features=json.dumps(prediction_dict["input_features"]),
        model_version=prediction_dict["model_version"]
    )

    db.add(prediction_record)
    db.commit()
    db.refresh(prediction_record)

    return prepare_shelf_life_response(prediction_record)

@router.get("/{inventory_id}", response_model=ShelfLifePredictionResponse)
def get_latest_shelf_life_prediction(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    inv = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory batch #{inventory_id} not found."
        )

    record = db.query(ShelfLifePrediction).filter(
        ShelfLifePrediction.inventory_id == inventory_id
    ).order_by(ShelfLifePrediction.created_at.desc()).first()

    if not record:
        # Generate initial prediction on the fly
        req = ShelfLifePredictionRequest(inventory_id=inventory_id)
        return generate_shelf_life_prediction(req, db=db, current_user=current_user)

    return prepare_shelf_life_response(record)

@router.get("/{inventory_id}/history", response_model=List[ShelfLifePredictionResponse])
def get_shelf_life_history(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    inv = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory batch #{inventory_id} not found."
        )

    records = db.query(ShelfLifePrediction).filter(
        ShelfLifePrediction.inventory_id == inventory_id
    ).order_by(ShelfLifePrediction.created_at.desc()).all()

    return [prepare_shelf_life_response(r) for r in records]
