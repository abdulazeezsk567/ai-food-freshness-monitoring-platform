from datetime import date, datetime
from typing import Dict, Any, List, Optional

BASE_SHELF_LIFE_DAYS = {
    "Fruits": 14,
    "Vegetables": 10,
    "Dairy Products": 7,
    "Meat & Poultry": 5,
    "Seafood": 3,
    "Bakery": 4,
    "Beverages": 30,
    "Pantry / Dry Goods": 90
}

OPTIMAL_STORAGE = {
    "Fruits": {"temp": 4.0, "humidity": 85.0, "condition": "Refrigerated"},
    "Vegetables": {"temp": 4.0, "humidity": 90.0, "condition": "Refrigerated"},
    "Dairy Products": {"temp": 3.0, "humidity": 80.0, "condition": "Refrigerated"},
    "Meat & Poultry": {"temp": 1.0, "humidity": 85.0, "condition": "Refrigerated"},
    "Seafood": {"temp": 0.5, "humidity": 90.0, "condition": "Refrigerated"},
    "Bakery": {"temp": 20.0, "humidity": 60.0, "condition": "Room Temperature"},
    "Beverages": {"temp": 4.0, "humidity": 70.0, "condition": "Refrigerated"},
    "Pantry / Dry Goods": {"temp": 20.0, "humidity": 50.0, "condition": "Room Temperature"}
}

def extract_shelf_life_features(
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
    Feature engineering layer extracting normalized features for the predictive shelf-life model.
    """
    base_days = BASE_SHELF_LIFE_DAYS.get(food_category, 10)
    optimal = OPTIMAL_STORAGE.get(food_category, {"temp": 4.0, "humidity": 85.0, "condition": "Refrigerated"})

    # Compute food age in days since purchase
    today = date.today()
    age_days = (today - purchase_date).days if purchase_date else storage_duration_days
    age_days = max(0, age_days)

    # Temperature delta from optimal storage (°C)
    temp_delta = storage_temperature - optimal["temp"]

    # Humidity delta from optimal storage (%)
    humidity_delta = abs(storage_humidity - optimal["humidity"])

    # Historical trend analysis
    trend = "Insufficient Data"
    degradation_rate_per_day = 0.0
    if historical_scores and len(historical_scores) >= 2:
        score_diff = historical_scores[-1] - historical_scores[0]
        if score_diff > 3:
            trend = "Improving"
        elif score_diff < -3:
            trend = "Declining"
            degradation_rate_per_day = abs(score_diff) / max(1, len(historical_scores) - 1)
        else:
            trend = "Stable"

    return {
        "food_category": food_category,
        "base_shelf_life_days": base_days,
        "freshness_score": freshness_score,
        "freshness_category": freshness_category,
        "spoilage_probability": spoilage_probability,
        "age_days": age_days,
        "storage_duration_days": storage_duration_days,
        "storage_temperature": storage_temperature,
        "optimal_temperature": optimal["temp"],
        "temp_delta": round(temp_delta, 1),
        "storage_humidity": storage_humidity,
        "optimal_humidity": optimal["humidity"],
        "humidity_delta": round(humidity_delta, 1),
        "packaging_type": packaging_type,
        "storage_condition": storage_condition,
        "optimal_storage_condition": optimal["condition"],
        "trend": trend,
        "degradation_rate_per_day": round(degradation_rate_per_day, 2),
        "historical_scores": historical_scores or []
    }
