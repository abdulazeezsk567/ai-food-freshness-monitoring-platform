from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

ALLOWED_STORAGE_CONDITIONS = {"Refrigerated", "Frozen", "Room Temperature", "Controlled Storage", "Unknown"}
ALLOWED_PACKAGING_TYPES = {
    "Standard Packaging", 
    "Vacuum Sealed", 
    "Aseptic Packaging", 
    "Modified Atmosphere Packaging (MAP)", 
    "Plastic Tray with Film", 
    "Paper Wrapping", 
    "Unpackaged / Loose"
}

class StorageConditionCreate(BaseModel):
    inventory_id: int
    temperature: float = Field(4.0, ge=-30.0, le=60.0)
    humidity: float = Field(85.0, ge=0.0, le=100.0)
    storage_location: str = "Cold Room A"
    packaging_type: str = "Standard Packaging"
    storage_condition: str = "Refrigerated"
    storage_duration_days: int = Field(1, ge=0)
    notes: Optional[str] = None

    @field_validator('storage_condition')
    @classmethod
    def validate_storage_condition(cls, v: str) -> str:
        if v not in ALLOWED_STORAGE_CONDITIONS:
            raise ValueError(f"Invalid storage_condition. Must be one of: {', '.join(sorted(ALLOWED_STORAGE_CONDITIONS))}")
        return v

    @field_validator('packaging_type')
    @classmethod
    def validate_packaging_type(cls, v: str) -> str:
        if v not in ALLOWED_PACKAGING_TYPES:
            raise ValueError(f"Invalid packaging_type. Must be one of: {', '.join(sorted(ALLOWED_PACKAGING_TYPES))}")
        return v

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
