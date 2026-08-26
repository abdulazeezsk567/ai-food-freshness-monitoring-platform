import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database.session import Base

class UserRole(str, enum.Enum):
    CONSUMER = "CONSUMER"
    RETAIL_MANAGER = "RETAIL_MANAGER"
    WAREHOUSE_OPERATOR = "WAREHOUSE_OPERATOR"
    FOOD_QUALITY_INSPECTOR = "FOOD_QUALITY_INSPECTOR"
    ADMINISTRATOR = "ADMINISTRATOR"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default=UserRole.CONSUMER.value)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    food_items = relationship("FoodItem", back_populates="creator", cascade="all, delete-orphan")
