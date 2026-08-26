from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    food_item_id = Column(Integer, ForeignKey("food_items.id", ondelete="CASCADE"), nullable=False)
    batch_number = Column(String(100), nullable=False, index=True)
    quantity = Column(Float, nullable=False, default=1.0)
    unit = Column(String(30), nullable=False, default="kg")
    purchase_date = Column(Date, nullable=False, default=date.today)
    expiry_date = Column(Date, nullable=False, index=True)
    storage_temperature = Column(Float, nullable=False, default=4.0)  # in °C
    storage_humidity = Column(Float, nullable=False, default=85.0)     # % relative humidity
    packaging_type = Column(String(100), nullable=False, default="Standard Packaging")
    storage_duration = Column(Integer, nullable=False, default=7)      # storage duration in days
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    food_item = relationship("FoodItem", back_populates="inventory_batches")
