from datetime import datetime, date
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict

class ShelfLifePredictionRequest(BaseModel):
    inventory_id: int
    analysis_id: Optional[int] = None
    temperature_override: Optional[float] = None
    humidity_override: Optional[float] = None
    storage_condition_override: Optional[str] = None

class ShelfLifePredictionResponse(BaseModel):
    id: int
    inventory_id: int
    analysis_id: Optional[int] = None
    user_id: int
    estimated_remaining_days: int
    estimated_expiry_date: date
    risk_level: str
    confidence: float
    trend: str
    storage_impact: Dict[str, Any]
    contributing_factors: Dict[str, Any]
    storage_guidance: List[str]
    input_features: Dict[str, Any]
    model_version: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
