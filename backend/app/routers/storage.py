from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.models.inventory import Inventory
from app.models.storage import StorageCondition
from app.schemas.storage import (
    StorageConditionCreate,
    StorageConditionResponse,
    BatchTelemetryIngestRequest,
    BatchTelemetryIngestResponse
)
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

@router.post("/batch-telemetry", response_model=BatchTelemetryIngestResponse, status_code=status.HTTP_201_CREATED)
@router.post("/simulate-stream", response_model=BatchTelemetryIngestResponse, status_code=status.HTTP_201_CREATED)
def ingest_batch_telemetry(
    data: BatchTelemetryIngestRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    inv = db.query(Inventory).filter(Inventory.id == data.inventory_id).first()
    if not inv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory batch #{data.inventory_id} not found."
        )

    alerts = []
    created_records = []

    for reading in data.readings:
        # Check temperature safety thresholds
        if reading.temperature > 8.0:
            alerts.append(f"Thermal breach: {reading.temperature}°C exceeds safety ceiling of 8.0°C")
        elif reading.temperature < 0.0 and inv.food_item and inv.food_item.category in ["Fruits", "Vegetables"]:
            alerts.append(f"Freezing hazard: {reading.temperature}°C may cause chill damage to produce")

        # Check humidity safety thresholds
        if reading.humidity > 95.0:
            alerts.append(f"High moisture warning: {reading.humidity}% RH exceeds 95% ceiling")
        elif reading.humidity < 40.0:
            alerts.append(f"Low humidity warning: {reading.humidity}% RH causes desiccation")

        rec = StorageCondition(
            inventory_id=data.inventory_id,
            user_id=current_user.id,
            temperature=reading.temperature,
            humidity=reading.humidity,
            storage_location=reading.storage_location or "Automated Sensor",
            packaging_type=reading.packaging_type or inv.packaging_type,
            storage_condition=reading.storage_condition or "Refrigerated",
            storage_duration_days=reading.storage_duration_days if reading.storage_duration_days is not None else inv.storage_duration,
            notes=f"[{data.sensor_id}] {reading.notes or 'Automated telemetry ingestion'}"
        )
        db.add(rec)
        created_records.append(rec)

    # Synchronize physical inventory batch with latest sensor state
    last_reading = data.readings[-1]
    inv.storage_temperature = last_reading.temperature
    inv.storage_humidity = last_reading.humidity
    if last_reading.packaging_type:
        inv.packaging_type = last_reading.packaging_type
    if last_reading.storage_duration_days is not None:
        inv.storage_duration = last_reading.storage_duration_days

    db.commit()

    return BatchTelemetryIngestResponse(
        inventory_id=data.inventory_id,
        sensor_id=data.sensor_id,
        ingested_count=len(created_records),
        latest_temperature=last_reading.temperature,
        latest_humidity=last_reading.humidity,
        alerts_triggered=sorted(list(set(alerts))),
        status="ingested_successfully"
    )

@router.get("/{inventory_id}", response_model=StorageConditionResponse)
def get_latest_storage_condition(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    record = db.query(StorageCondition).filter(
        StorageCondition.inventory_id == inventory_id
    ).order_by(StorageCondition.created_at.desc(), StorageCondition.id.desc()).first()

    if not record:
        inv = db.query(Inventory).filter(Inventory.id == inventory_id).first()
        if not inv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inventory batch #{inventory_id} not found."
            )
        
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
