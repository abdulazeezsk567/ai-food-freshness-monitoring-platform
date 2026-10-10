import csv
import io
import json
from datetime import datetime, date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload

from app.database.session import get_db
from app.models.user import User
from app.models.inventory import Inventory
from app.models.food_item import FoodItem
from app.models.analysis import AnalysisResult
from app.models.shelf_life import ShelfLifePrediction
from app.core.security import get_current_active_user
from app.routers.inventory import compute_inventory_status

router = APIRouter(prefix="/api/reports", tags=["Downloadable Reports & Data Exports"])

@router.get("/inventory/csv")
def export_inventory_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Exports full active physical food inventory records as an RFC-4180 compliant CSV stream.
    """
    items = db.query(Inventory).options(joinedload(Inventory.food_item)).order_by(Inventory.expiry_date.asc()).all()

    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

    # Write Header row
    writer.writerow([
        "Batch Number",
        "Food Item",
        "Category",
        "Quantity",
        "Unit",
        "Purchase Date",
        "Expiry Date",
        "Days to Expiry",
        "Freshness Status",
        "Storage Temp (C)",
        "Storage Humidity (%)",
        "Packaging Type",
        "Storage Duration (Days)",
        "Registered At"
    ])

    for item in items:
        days_left, status_label = compute_inventory_status(item)
        writer.writerow([
            item.batch_number,
            item.food_item.name if item.food_item else "Unknown",
            item.food_item.category if item.food_item else "Uncategorized",
            item.quantity,
            item.unit,
            str(item.purchase_date),
            str(item.expiry_date),
            days_left,
            status_label,
            item.storage_temperature,
            item.storage_humidity,
            item.packaging_type,
            item.storage_duration,
            item.created_at.strftime("%Y-%m-%d %H:%M:%S") if item.created_at else ""
        ])

    csv_data = output.getvalue()
    filename = f"food_inventory_report_{date.today().isoformat()}.csv"

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )

@router.get("/freshness/{analysis_id}/json")
def export_freshness_report_json(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Downloads formal computer vision inspection assessment certificate as a formatted JSON document.
    """
    record = db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis result #{analysis_id} not found."
        )

    color_dict = json.loads(record.color_analysis) if isinstance(record.color_analysis, str) else record.color_analysis
    texture_dict = json.loads(record.texture_analysis) if isinstance(record.texture_analysis, str) else record.texture_analysis
    spoilage_dict = json.loads(record.spoilage_indicators) if isinstance(record.spoilage_indicators, str) else record.spoilage_indicators

    payload = {
        "metadata": {
            "report_type": "Computer Vision Freshness Inspection Certificate",
            "report_id": f"AN-{record.id}",
            "exported_at": datetime.utcnow().isoformat() + "Z",
            "exported_by": current_user.email,
            "engine_version": record.model_version or "v1.0.0-CV",
            "platform": "AI-Powered Food Freshness Monitoring Platform"
        },
        "inspection_certificate": {
            "id": record.id,
            "inventory_id": record.inventory_id,
            "food_category": record.food_category,
            "image_path": record.image_path,
            "classification_status": record.predicted_category,
            "freshness_score": record.freshness_score,
            "spoilage_probability": record.spoilage_probability,
            "confidence": record.confidence,
            "color_analysis": color_dict,
            "texture_analysis": texture_dict,
            "spoilage_indicators": spoilage_dict,
            "created_at": record.created_at.isoformat() if record.created_at else None
        }
    }

    content_str = json.dumps(payload, indent=2)
    filename = f"freshness_inspection_report_{record.id}.json"

    return Response(
        content=content_str,
        media_type="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )

@router.get("/shelf-life/{prediction_id}/json")
def export_shelf_life_report_json(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Downloads deterministic predictive shelf-life forecast certificate as a formatted JSON document.
    """
    record = db.query(ShelfLifePrediction).filter(ShelfLifePrediction.id == prediction_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shelf life prediction record #{prediction_id} not found."
        )

    storage_impact_val = json.loads(record.storage_impact) if isinstance(record.storage_impact, str) else record.storage_impact
    contributing_factors_val = json.loads(record.contributing_factors) if isinstance(record.contributing_factors, str) else record.contributing_factors
    storage_guidance_val = json.loads(record.storage_guidance) if isinstance(record.storage_guidance, str) else record.storage_guidance
    input_features_val = json.loads(record.input_features) if isinstance(record.input_features, str) else record.input_features

    payload = {
        "metadata": {
            "report_type": "Predictive Shelf-Life Forecast Report",
            "report_id": f"SLP-{record.id}",
            "exported_at": datetime.utcnow().isoformat() + "Z",
            "exported_by": current_user.email,
            "model_version": record.model_version,
            "model_architecture": "Deterministic Multi-Factor Baseline Model (shelf-life-baseline-v1)",
            "safety_disclaimer": "AI/Model Estimate — Not a Food Safety Certification. Operational forecasting only."
        },
        "forecast_data": {
            "prediction_id": record.id,
            "inventory_id": record.inventory_id,
            "analysis_id": record.analysis_id,
            "estimated_remaining_days": record.estimated_remaining_days,
            "estimated_expiry_date": str(record.estimated_expiry_date),
            "risk_level": record.risk_level,
            "heuristic_baseline_confidence": record.confidence,
            "degradation_trend": record.trend,
            "storage_impact_decomposition": storage_impact_val,
            "contributing_factors": contributing_factors_val,
            "actionable_guidance": storage_guidance_val,
            "input_features_snapshot": input_features_val,
            "created_at": record.created_at.isoformat() if record.created_at else None
        }
    }

    content_str = json.dumps(payload, indent=2)
    filename = f"shelf_life_prediction_report_{record.id}.json"

    return Response(
        content=content_str,
        media_type="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )
