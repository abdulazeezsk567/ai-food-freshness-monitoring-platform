import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class FoodCategory(str, enum.Enum):
    FRUITS = "Fruits"
    VEGETABLES = "Vegetables"
    DAIRY = "Dairy Products"
    MEAT_POULTRY = "Meat & Poultry"
    SEAFOOD = "Seafood"
    BAKERY = "Bakery Products"
    PACKAGED = "Packaged Foods"
    BEVERAGES = "Beverages"

class FoodItem(Base):
    __tablename__ = "food_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    creator = relationship("User", back_populates="food_items")
    inventory_batches = relationship("Inventory", back_populates="food_item", cascade="all, delete-orphan")
