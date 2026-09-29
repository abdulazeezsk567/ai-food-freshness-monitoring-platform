from typing import Dict, Any, List, Optional
from datetime import date

from app.ml.shelf_life_features import extract_shelf_life_features
from app.ml.shelf_life_model import predict_shelf_life, MODEL_VERSION

def run_shelf_life_prediction(
    food_category: str,
    freshness_score: int,
    freshness_category: str,
    spoilage_probability: float,
    has_image_analysis: bool = False,
    has_storage_log: bool = False,
    purchase_date: Optional[date] = None,
    storage_temperature: float = 4.0,
    storage_humidity: float = 85.0,
    packaging_type: str = "Standard Packaging",
    storage_condition: str = "Refrigerated",
    storage_duration_days: int = 1,
    past_analysis_records: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Executes the Milestone 3 Predictive Shelf-Life Monitoring Pipeline (shelf-life-baseline-v1):
    Extract Features -> Run Deterministic Heuristic Model -> Risk Classification -> Storage Impact & Guidance.
    """
    features = extract_shelf_life_features(
        food_category=food_category,
        freshness_score=freshness_score,
        freshness_category=freshness_category,
        spoilage_probability=spoilage_probability,
        has_image_analysis=has_image_analysis,
        has_storage_log=has_storage_log,
        purchase_date=purchase_date,
        storage_temperature=storage_temperature,
        storage_humidity=storage_humidity,
        packaging_type=packaging_type,
        storage_condition=storage_condition,
        storage_duration_days=storage_duration_days,
        past_analysis_records=past_analysis_records
    )

    prediction = predict_shelf_life(features)
    return prediction
