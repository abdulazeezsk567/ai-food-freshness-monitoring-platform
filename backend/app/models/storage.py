from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class StorageCondition(Base):
    __tablename__ = "storage_conditions"

    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    temperature = Column(Float, nullable=False, default=4.0)       # in °C
    humidity = Column(Float, nullable=False, default=85.0)          # % relative humidity
    storage_location = Column(String(100), nullable=False, default="Cold Room A")
    packaging_type = Column(String(100), nullable=False, default="Standard Packaging")
    storage_condition = Column(String(50), nullable=False, default="Refrigerated")  # Refrigerated, Frozen, Room Temperature, Controlled Storage, Unknown
    storage_duration_days = Column(Integer, nullable=False, default=1)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    inventory = relationship("Inventory")
    user = relationship("User")
