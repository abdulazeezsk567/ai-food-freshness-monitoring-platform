from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.models.inventory import Inventory
from app.models.storage import StorageCondition
from app.schemas.storage import StorageConditionCreate, StorageConditionResponse
from app.core.security import get_current_active_user

router = APIRouter(prefix="/api/storage-conditions", tags=["Storage Condition Monitoring"])

@router.post("", response_model=StorageConditionResponse, status_code=status.HTTP_201_CREATED)
def record_storage_condition(
    data: StorageConditionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    inv = db.query(Inventory).filter(Inventory.id == data.inventory_id).first()
    if not inv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory batch #{data.inventory_id} not found."
        )

    # Update inventory batch fields as well for real-time consistency
    inv.storage_temperature = data.temperature
    inv.storage_humidity = data.humidity
    inv.packaging_type = data.packaging_type
    inv.storage_duration = data.storage_duration_days

    storage_record = StorageCondition(
        inventory_id=data.inventory_id,
        user_id=current_user.id,
        temperature=data.temperature,
        humidity=data.humidity,
        storage_location=data.storage_location,
        packaging_type=data.packaging_type,
        storage_condition=data.storage_condition,
        storage_duration_days=data.storage_duration_days,
        notes=data.notes
    )

    db.add(storage_record)
    db.commit()
    db.refresh(storage_record)

    return storage_record

@router.get("/{inventory_id}", response_model=StorageConditionResponse)
def get_latest_storage_condition(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    record = db.query(StorageCondition).filter(
        StorageCondition.inventory_id == inventory_id
    ).order_by(StorageCondition.created_at.desc()).first()

    if not record:
        # Fallback to inventory batch defaults if no custom log exists yet
        inv = db.query(Inventory).filter(Inventory.id == inventory_id).first()
        if not inv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inventory batch #{inventory_id} not found."
            )
        
        # Create virtual record
        return StorageConditionResponse(
            id=0,
            inventory_id=inv.id,
            user_id=current_user.id,
            temperature=inv.storage_temperature,
            humidity=inv.storage_humidity,
            storage_location="Default Storage Room",
            packaging_type=inv.packaging_type,
            storage_condition="Refrigerated",
            storage_duration_days=inv.storage_duration,
            notes="Default batch environment telemetry",
            created_at=inv.created_at
        )

    return record

@router.get("/{inventory_id}/history", response_model=List[StorageConditionResponse])
def get_storage_condition_history(
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

    records = db.query(StorageCondition).filter(
        StorageCondition.inventory_id == inventory_id
    ).order_by(StorageCondition.created_at.desc()).all()

    return records
