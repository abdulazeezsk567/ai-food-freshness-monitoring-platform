from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class StorageConditionCreate(BaseModel):
    inventory_id: int
    temperature: float = 4.0
    humidity: float = 85.0
    storage_location: str = "Cold Room A"
    packaging_type: str = "Standard Packaging"
    storage_condition: str = "Refrigerated"  # Refrigerated, Frozen, Room Temperature, Controlled Storage, Unknown
    storage_duration_days: int = 1
    notes: Optional[str] = None

class StorageConditionResponse(BaseModel):
    id: int
    inventory_id: int
    user_id: int
    temperature: float
    humidity: float
    storage_location: str
    packaging_type: str
    storage_condition: str
    storage_duration_days: int
    notes: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
