from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Float, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class ShelfLifePrediction(Base):
    __tablename__ = "shelf_life_predictions"

    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id", ondelete="CASCADE"), nullable=False, index=True)
    analysis_id = Column(Integer, ForeignKey("analysis_results.id", ondelete="SET NULL"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    estimated_remaining_days = Column(Integer, nullable=False)
    estimated_expiry_date = Column(Date, nullable=False)
    risk_level = Column(String(50), nullable=False, index=True)  # LOW RISK, MEDIUM RISK, HIGH RISK, CRITICAL
    confidence = Column(Float, nullable=False, default=0.85)
    trend = Column(String(50), nullable=False, default="Stable")   # Improving, Stable, Declining, Insufficient Data

    storage_impact = Column(Text, nullable=False)        # JSON stringified
    contributing_factors = Column(Text, nullable=False)  # JSON stringified
    storage_guidance = Column(Text, nullable=False)      # JSON stringified
    input_features = Column(Text, nullable=False)        # JSON stringified

    model_version = Column(String(50), nullable=False, default="shelf-life-baseline-v1")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    inventory = relationship("Inventory")
    analysis = relationship("AnalysisResult")
    user = relationship("User")
