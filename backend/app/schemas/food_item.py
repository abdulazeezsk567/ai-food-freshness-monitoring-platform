from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class FoodItemBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None

class FoodItemCreate(FoodItemBase):
    pass

class FoodItemUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None

class FoodItemResponse(FoodItemBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
