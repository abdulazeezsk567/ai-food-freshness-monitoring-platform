from datetime import datetime, date
from typing import Optional, Dict, Any, List
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

class ShelfLifePredictionRequest(BaseModel):
    inventory_id: int
    analysis_id: Optional[int] = None
    temperature_override: Optional[float] = Field(None, ge=-30.0, le=60.0)
    humidity_override: Optional[float] = Field(None, ge=0.0, le=100.0)
    storage_condition_override: Optional[str] = None
    packaging_type_override: Optional[str] = None

    @field_validator('storage_condition_override')
    @classmethod
    def validate_storage_condition(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ALLOWED_STORAGE_CONDITIONS:
            raise ValueError(f"Invalid storage_condition. Must be one of: {', '.join(sorted(ALLOWED_STORAGE_CONDITIONS))}")
        return v

    @field_validator('packaging_type_override')
    @classmethod
    def validate_packaging_type(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ALLOWED_PACKAGING_TYPES:
            raise ValueError(f"Invalid packaging_type. Must be one of: {', '.join(sorted(ALLOWED_PACKAGING_TYPES))}")
        return v

class ShelfLifePredictionResponse(BaseModel):
    id: int
    inventory_id: int
    analysis_id: Optional[int] = None
    user_id: int
    estimated_remaining_days: int = Field(..., ge=0)
    estimated_expiry_date: date
    risk_level: str
    confidence: float
    trend: str
    has_image_analysis: bool = False
    has_storage_log: bool = False
    degradation_rate_per_day: Optional[float] = None
    sufficient_data: bool = False
    storage_impact: Dict[str, Any]
    contributing_factors: Dict[str, Any]
    storage_guidance: List[str]
    input_features: Dict[str, Any]
    model_version: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
