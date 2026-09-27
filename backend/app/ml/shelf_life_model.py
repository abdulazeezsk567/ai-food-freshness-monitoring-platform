from datetime import date, timedelta
from typing import Dict, Any, List, Tuple

MODEL_VERSION = "shelf-life-baseline-v1"

def predict_shelf_life(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predictive shelf-life model (shelf-life-baseline-v1) calculating estimated remaining
    days, estimated expiry date, risk level, degradation trend, storage impact, and guidance.
    """
    base_days = features["base_shelf_life_days"]
    freshness_score = features["freshness_score"]
    spoilage_prob = features["spoilage_probability"]
    age_days = features["age_days"]
    temp_delta = features["temp_delta"]
    humidity_delta = features["humidity_delta"]
    packaging = features["packaging_type"]
    condition = features["storage_condition"]
    optimal_condition = features["optimal_storage_condition"]
    trend = features["trend"]

    # 1. Temperature Impact Factor
    if temp_delta > 0:
        temp_factor = max(0.2, 1.0 - (temp_delta * 0.08))
    else:
        temp_factor = min(1.1, 1.0 + (abs(temp_delta) * 0.02))

    # 2. Humidity Impact Factor
    humidity_factor = max(0.4, 1.0 - (humidity_delta * 0.015))

    # 3. Packaging Factor
    pkg_factors = {
        "Vacuum Sealed": 1.20,
        "Aseptic Packaging": 1.15,
        "Modified Atmosphere Packaging (MAP)": 1.10,
        "Plastic Tray with Film": 1.0,
        "Standard Packaging": 1.0,
        "Paper Wrapping": 0.90,
        "Unpackaged / Loose": 0.80
    }
    pkg_factor = pkg_factors.get(packaging, 1.0)

    # 4. Storage Condition Factor
    if condition == "Frozen":
        cond_factor = 1.8 if optimal_condition != "Frozen" else 1.0
    elif condition == optimal_condition:
        cond_factor = 1.0
    elif condition == "Room Temperature" and optimal_condition == "Refrigerated":
        cond_factor = 0.45  # Severe penalty for non-refrigerated perishable item
    else:
        cond_factor = 0.85

    # 5. Calculate Remaining Days
    freshness_ratio = max(0.0, min(1.0, freshness_score / 100.0))
    raw_remaining = (base_days * freshness_ratio * temp_factor * humidity_factor * pkg_factor * cond_factor) - age_days
    remaining_days = max(0, int(round(raw_remaining)))

    # 6. Estimated Expiry Date
    estimated_expiry = date.today() + timedelta(days=remaining_days)

    # 7. Risk Level Classification
    if remaining_days <= 1 or spoilage_prob >= 0.70 or freshness_score < 40:
        risk_level = "CRITICAL"
    elif remaining_days <= 3 or spoilage_prob >= 0.45 or freshness_score < 60 or (trend == "Declining" and freshness_score < 70):
        risk_level = "HIGH RISK"
    elif remaining_days <= 7 or spoilage_prob >= 0.25 or temp_delta > 3.0:
        risk_level = "MEDIUM RISK"
    else:
        risk_level = "LOW RISK"

    # 8. Storage Impact Explanation & Factors
    storage_impact_observations = []
    if temp_delta > 2.0:
        storage_impact_observations.append(
            f"Storage temperature ({features['storage_temperature']}°C) is {temp_delta}°C higher than optimal ({features['optimal_temperature']}°C), accelerating degradation."
        )
    elif temp_delta < -1.0:
        storage_impact_observations.append(
            f"Cold storage temperature ({features['storage_temperature']}°C) provides favorable preservation."
        )

    if humidity_delta > 15.0:
        storage_impact_observations.append(
            f"Relative humidity ({features['storage_humidity']}%) deviates significantly from recommended {features['optimal_humidity']}%, affecting texture."
        )

    if condition == "Room Temperature" and optimal_condition == "Refrigerated":
        storage_impact_observations.append(
            "Item is stored at Room Temperature instead of recommended Refrigerated cold-chain storage."
        )

    if not storage_impact_observations:
        storage_impact_observations.append(
            "Storage temperature, humidity, and packaging format are within optimal configured preservation ranges."
        )

    storage_impact = {
        "temperature_factor": round(temp_factor, 2),
        "humidity_factor": round(humidity_factor, 2),
        "packaging_factor": round(pkg_factor, 2),
        "condition_factor": round(cond_factor, 2),
        "observations": storage_impact_observations
    }

    # 9. Contributing Factors Breakdown
    contributing_factors = {
        "freshness_score_weight": f"{freshness_score}/100",
        "spoilage_probability": f"{spoilage_prob * 100:.1f}%",
        "product_age_days": age_days,
        "base_category_shelf_life": f"{base_days} days",
        "historical_trend": trend
    }

    # 10. Conservative Storage Guidance
    guidance = []
    if risk_level in ["CRITICAL", "HIGH RISK"]:
        guidance.append("Inspect item immediately and prioritize for consumption or retail clearance.")
    if temp_delta > 2.0:
        guidance.append(f"Lower storage temperature closer to optimal {features['optimal_temperature']}°C.")
    if condition == "Room Temperature" and optimal_condition == "Refrigerated":
        guidance.append("Transfer item to refrigerated storage immediately to slow decay.")
    if not guidance:
        guidance.append("Maintain current cold-chain storage conditions and monitor regularly.")

    # 11. Prediction Confidence (based on feature completeness & historical score availability)
    confidence = 0.90 if trend != "Insufficient Data" else 0.82
    if freshness_score < 30:
        confidence = 0.95  # High certainty of decay

    return {
        "estimated_remaining_days": remaining_days,
        "estimated_expiry_date": estimated_expiry.isoformat(),
        "risk_level": risk_level,
        "confidence": confidence,
        "trend": trend,
        "storage_impact": storage_impact,
        "contributing_factors": contributing_factors,
        "storage_guidance": guidance,
        "input_features": features,
        "model_version": MODEL_VERSION
    }
