from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.food_item import FoodItemResponse

class InventoryBase(BaseModel):
    food_item_id: int
    batch_number: str
    quantity: float = 1.0
    unit: str = "kg"
    purchase_date: date
    expiry_date: date
    storage_temperature: float = 4.0
    storage_humidity: float = 85.0
    packaging_type: str = "Standard Packaging"
    storage_duration: int = 7

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    food_item_id: Optional[int] = None
    batch_number: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    purchase_date: Optional[date] = None
    expiry_date: Optional[date] = None
    storage_temperature: Optional[float] = None
    storage_humidity: Optional[float] = None
    packaging_type: Optional[str] = None
    storage_duration: Optional[int] = None

class InventoryResponse(InventoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    food_item: Optional[FoodItemResponse] = None
    days_to_expiry: Optional[int] = None
    status: Optional[str] = None  # Fresh, Good, Acceptable, Near Spoilage, Spoiled

    model_config = ConfigDict(from_attributes=True)
