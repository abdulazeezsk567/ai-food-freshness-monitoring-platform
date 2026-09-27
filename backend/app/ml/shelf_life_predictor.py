from typing import Dict, Any, List, Optional
from datetime import date

from app.ml.shelf_life_features import extract_shelf_life_features
from app.ml.shelf_life_model import predict_shelf_life, MODEL_VERSION

def run_shelf_life_prediction(
    food_category: str,
    freshness_score: int,
    freshness_category: str,
    spoilage_probability: float,
    purchase_date: Optional[date] = None,
    storage_temperature: float = 4.0,
    storage_humidity: float = 85.0,
    packaging_type: str = "Standard Packaging",
    storage_condition: str = "Refrigerated",
    storage_duration_days: int = 1,
    historical_scores: Optional[List[int]] = None
) -> Dict[str, Any]:
    """
    Executes the full Milestone 3 Predictive Shelf-Life Monitoring Pipeline:
    Extract Features -> Execute Baseline Prediction Formula -> Risk Classification -> Storage Impact & Guidance.
    """
    features = extract_shelf_life_features(
        food_category=food_category,
        freshness_score=freshness_score,
        freshness_category=freshness_category,
        spoilage_probability=spoilage_probability,
        purchase_date=purchase_date,
        storage_temperature=storage_temperature,
        storage_humidity=storage_humidity,
        packaging_type=packaging_type,
        storage_condition=storage_condition,
        storage_duration_days=storage_duration_days,
        historical_scores=historical_scores
    )

    prediction = predict_shelf_life(features)
    return prediction
