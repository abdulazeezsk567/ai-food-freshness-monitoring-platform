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

ALLOWED_STORAGE_CONDITIONS = {"Refrigerated", "Frozen", "Room Temperature", "Controlled Storage", "Unknown"}
ALLOWED_PACKAGING_TYPES = {
    "Standard Packaging", 
    "Vacuum Sealed", 
    "Aseptic Packaging", 
    "Modified Atmosphere Packaging (MAP)", 
    "Plastic Tray with Film", 
    "Paper Wrapping", 
    "Unpackaged / Loose"
}

def extract_shelf_life_features(
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
    Feature engineering layer extracting normalized features for shelf-life-baseline-v1.
    Includes timestamp-based degradation velocity and feature-completeness indicators.
    """
    # Validation & normalization
    freshness_score = max(0, min(100, int(freshness_score)))
    spoilage_probability = max(0.0, min(1.0, float(spoilage_probability)))
    storage_humidity = max(0.0, min(100.0, float(storage_humidity)))
    storage_temperature = max(-30.0, min(60.0, float(storage_temperature)))
    storage_duration_days = max(0, int(storage_duration_days))

    if storage_condition not in ALLOWED_STORAGE_CONDITIONS:
        storage_condition = "Refrigerated"
    if packaging_type not in ALLOWED_PACKAGING_TYPES:
        packaging_type = "Standard Packaging"

    base_days = BASE_SHELF_LIFE_DAYS.get(food_category, 10)
    optimal = OPTIMAL_STORAGE.get(food_category, {"temp": 4.0, "humidity": 85.0, "condition": "Refrigerated"})

    # Compute food age in days since purchase date or cumulative storage duration
    today = date.today()
    age_days = (today - purchase_date).days if purchase_date else storage_duration_days
    age_days = max(0, age_days)

    # Temperature and Humidity deltas
    temp_delta = storage_temperature - optimal["temp"]
    humidity_delta = abs(storage_humidity - optimal["humidity"])

    # Timestamp-based degradation rate calculation
    trend = "Insufficient Data"
    degradation_rate_per_day: Optional[float] = None
    sufficient_data = False

    if past_analysis_records and len(past_analysis_records) >= 2:
        # Sort by timestamp ascending
        sorted_records = sorted(past_analysis_records, key=lambda x: x["created_at"])
        first_rec = sorted_records[0]
        last_rec = sorted_records[-1]

        t_first: datetime = first_rec["created_at"]
        t_last: datetime = last_rec["created_at"]

        # Calculate actual elapsed days
        elapsed_seconds = (t_last - t_first).total_seconds()
        elapsed_days = elapsed_seconds / 86400.0

        score_change = last_rec["freshness_score"] - first_rec["freshness_score"]

        if elapsed_days > 0.001:  # Non-trivial time gap
            rate = abs(score_change) / elapsed_days
            degradation_rate_per_day = round(rate, 2)
            sufficient_data = True

            if score_change < -3:
                trend = "Declining"
            elif score_change > 3:
                trend = "Improving"
            else:
                trend = "Stable"
        else:
            # Assessments created almost simultaneously
            trend = "Insufficient Data"
            degradation_rate_per_day = 0.0
            sufficient_data = False

    return {
        "food_category": food_category,
        "base_shelf_life_days": base_days,
        "freshness_score": freshness_score,
        "freshness_category": freshness_category,
        "spoilage_probability": spoilage_probability,
        "has_image_analysis": has_image_analysis,
        "has_storage_log": has_storage_log,
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
        "degradation_rate_per_day": degradation_rate_per_day,
        "sufficient_data": sufficient_data
    }
