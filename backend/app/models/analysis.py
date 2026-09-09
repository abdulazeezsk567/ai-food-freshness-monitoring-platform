from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id", ondelete="SET NULL"), nullable=True, index=True)
    
    image_path = Column(String(500), nullable=False)
    food_category = Column(String(50), nullable=False, index=True)
    predicted_category = Column(String(50), nullable=False, index=True)
    freshness_score = Column(Integer, nullable=False)  # 0 to 100
    spoilage_probability = Column(Float, nullable=False)  # 0.0 to 1.0
    confidence = Column(Float, nullable=False)  # 0.0 to 1.0
    
    color_analysis = Column(Text, nullable=False)       # JSON stringified
    texture_analysis = Column(Text, nullable=False)     # JSON stringified
    spoilage_indicators = Column(Text, nullable=False)  # JSON stringified
    
    model_version = Column(String(50), nullable=False, default="v1.0.0-CV")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User")
    inventory = relationship("Inventory")
