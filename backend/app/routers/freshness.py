import os
import uuid
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.models.inventory import Inventory
from app.models.analysis import AnalysisResult
from app.schemas.freshness import AnalysisResultResponse, AnalysisUploadResponse
from app.core.security import get_current_active_user
from app.ml import run_freshness_pipeline, validate_image_file

router = APIRouter(prefix="/api/freshness", tags=["Freshness Analysis & CV Engine"])

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "freshness"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def prepare_analysis_response(record: AnalysisResult) -> AnalysisResultResponse:
    color_dict = json.loads(record.color_analysis) if isinstance(record.color_analysis, str) else record.color_analysis
    texture_dict = json.loads(record.texture_analysis) if isinstance(record.texture_analysis, str) else record.texture_analysis
    spoilage_dict = json.loads(record.spoilage_indicators) if isinstance(record.spoilage_indicators, str) else record.spoilage_indicators

    return AnalysisResultResponse(
        id=record.id,
        user_id=record.user_id,
        inventory_id=record.inventory_id,
        image_path=record.image_path,
        food_category=record.food_category,
        predicted_category=record.predicted_category,
        freshness_score=record.freshness_score,
        spoilage_probability=record.spoilage_probability,
        confidence=record.confidence,
        color_analysis=color_dict,
        texture_analysis=texture_dict,
        spoilage_indicators=spoilage_dict,
        model_version=record.model_version,
        created_at=record.created_at
    )

@router.post("/upload", response_model=AnalysisUploadResponse)
async def upload_food_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{file.content_type}'. Allowed types: JPG, PNG, WEBP."
        )

    contents = await file.read()
    file_size = len(contents)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds 10MB limit ({file_size / (1024*1024):.2f}MB provided)."
        )

    ext = os.path.splitext(file.filename)[1].lower()
    if not ext or ext not in {".jpg", ".jpeg", ".png", ".webp"}:
        ext = ".jpg"

    safe_filename = f"{uuid.uuid4().hex}{ext}"
    dest_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(dest_path, "wb") as f:
        f.write(contents)

    rel_image_path = f"/uploads/freshness/{safe_filename}"
    return {
        "image_path": rel_image_path,
        "file_name": file.filename,
        "file_size_bytes": file_size,
        "content_type": file.content_type
    }

@router.post("/analyze", response_model=AnalysisResultResponse, status_code=status.HTTP_201_CREATED)
async def analyze_food_freshness(
    file: Optional[UploadFile] = File(None),
    image_path: Optional[str] = Form(None),
    food_category: str = Form("Fruits"),
    inventory_id: Optional[int] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    target_disk_path = None
    rel_path = None

    if file:
        upload_meta = await upload_food_image(file, current_user)
        rel_path = upload_meta["image_path"]
        filename = os.path.basename(rel_path)
        target_disk_path = os.path.join(UPLOAD_DIR, filename)
    elif image_path:
        rel_path = image_path
        filename = os.path.basename(image_path)
        target_disk_path = os.path.join(UPLOAD_DIR, filename)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either an image file upload or image_path must be provided."
        )

    if not os.path.exists(target_disk_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Uploaded image file does not exist at path '{target_disk_path}'."
        )

    # Optional Inventory Link Validation
    if inventory_id:
        inv = db.query(Inventory).filter(Inventory.id == inventory_id).first()
        if not inv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inventory batch record #{inventory_id} not found."
            )

    # Run ML & Computer Vision Pipeline
    try:
        report = run_freshness_pipeline(target_disk_path, food_category=food_category)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image analysis pipeline failed: {str(e)}"
        )

    # Create Database Record
    analysis_record = AnalysisResult(
        user_id=current_user.id,
        inventory_id=inventory_id,
        image_path=rel_path,
        food_category=food_category,
        predicted_category=report["predicted_category"],
        freshness_score=report["freshness_score"],
        spoilage_probability=report["spoilage_probability"],
        confidence=report["confidence"],
        color_analysis=json.dumps(report["color_analysis"]),
        texture_analysis=json.dumps(report["texture_analysis"]),
        spoilage_indicators=json.dumps(report["spoilage_indicators"]),
        model_version=report["model_version"]
    )

    db.add(analysis_record)
    db.commit()
    db.refresh(analysis_record)

    return prepare_analysis_response(analysis_record)

@router.get("/results", response_model=List[AnalysisResultResponse])
def list_analysis_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(AnalysisResult)
    if current_user.role not in ["ADMINISTRATOR", "FOOD_QUALITY_INSPECTOR"]:
        query = query.filter(AnalysisResult.user_id == current_user.id)

    results = query.order_by(AnalysisResult.created_at.desc()).all()
    return [prepare_analysis_response(r) for r in results]

@router.get("/results/{analysis_id}", response_model=AnalysisResultResponse)
def get_analysis_result(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis result record not found.")

    if current_user.role not in ["ADMINISTRATOR", "FOOD_QUALITY_INSPECTOR"] and result.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied to this analysis record.")

    return prepare_analysis_response(result)

@router.delete("/results/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_analysis_result(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = db.query(AnalysisResult).filter(AnalysisResult.id == analysis_id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis result record not found.")

    if current_user.role not in ["ADMINISTRATOR", "FOOD_QUALITY_INSPECTOR"] and result.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")

    # Remove stored image file if exists
    filename = os.path.basename(result.image_path)
    disk_file = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(disk_file):
        try:
            os.remove(disk_file)
        except Exception:
            pass

    db.delete(result)
    db.commit()
    return None

@router.get("/inventory/{inventory_id}/freshness-history", response_model=List[AnalysisResultResponse])
def get_inventory_freshness_history(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    inv = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory batch record not found.")

    results = db.query(AnalysisResult).filter(
        AnalysisResult.inventory_id == inventory_id
    ).order_by(AnalysisResult.created_at.desc()).all()

    return [prepare_analysis_response(r) for r in results]
