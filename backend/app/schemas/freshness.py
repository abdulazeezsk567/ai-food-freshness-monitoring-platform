from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict

class AnalysisUploadResponse(BaseModel):
    image_path: str
    file_name: str
    file_size_bytes: int
    content_type: str

class AnalysisRequest(BaseModel):
    image_path: str
    food_category: Optional[str] = "Fruits"
    inventory_id: Optional[int] = None

class AnalysisResultResponse(BaseModel):
    id: int
    user_id: int
    inventory_id: Optional[int] = None
    image_path: str
    food_category: str
    predicted_category: str
    freshness_score: int
    spoilage_probability: float
    confidence: float
    color_analysis: Dict[str, Any]
    texture_analysis: Dict[str, Any]
    spoilage_indicators: Dict[str, Any]
    model_version: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
