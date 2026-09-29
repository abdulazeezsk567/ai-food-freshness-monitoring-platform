from datetime import date, timedelta
from typing import Dict, Any, List

MODEL_VERSION = "shelf-life-baseline-v1"

def predict_shelf_life(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic predictive shelf-life baseline model (shelf-life-baseline-v1).
    
    Formula:
    remaining_days = max(0, (base_days * freshness_factor * spoilage_factor * temp_factor *
                             humidity_factor * packaging_factor * condition_factor * trend_factor) - age_days)
    """
    base_days = features["base_shelf_life_days"]
    freshness_score = features["freshness_score"]
    spoilage_prob = features["spoilage_probability"]
    has_image_analysis = features.get("has_image_analysis", False)
    has_storage_log = features.get("has_storage_log", False)
    age_days = features["age_days"]
    temp_delta = features["temp_delta"]
    humidity_delta = features["humidity_delta"]
    packaging = features["packaging_type"]
    condition = features["storage_condition"]
    optimal_condition = features["optimal_storage_condition"]
    trend = features["trend"]
    deg_rate = features.get("degradation_rate_per_day")
    sufficient_data = features.get("sufficient_data", False)

    # 1. Freshness Factor (Derived from visual image analysis if available)
    if has_image_analysis:
        freshness_factor = max(0.0, min(1.0, freshness_score / 100.0))
    else:
        freshness_factor = 1.0  # Storage-only baseline assumes baseline starting quality

    # 2. Spoilage Probability Impact Factor
    # Higher spoilage probability directly penalizes remaining shelf life
    spoilage_factor = max(0.1, 1.0 - (spoilage_prob * 0.85))

    # 3. Temperature Impact Factor
    if temp_delta > 0:
        # Temperature above optimal accelerates decay
        temp_factor = max(0.1, 1.0 - (temp_delta * 0.08))
    else:
        # Cold temperature below optimal provides preservation boost (up to 1.2x)
        temp_factor = min(1.2, 1.0 + (abs(temp_delta) * 0.02))

    # 4. Humidity Impact Factor
    humidity_factor = max(0.3, 1.0 - (humidity_delta * 0.015))

    # 5. Packaging Impact Factor
    pkg_factors = {
        "Vacuum Sealed": 1.25,
        "Aseptic Packaging": 1.15,
        "Modified Atmosphere Packaging (MAP)": 1.10,
        "Plastic Tray with Film": 1.0,
        "Standard Packaging": 1.0,
        "Paper Wrapping": 0.85,
        "Unpackaged / Loose": 0.70
    }
    pkg_factor = pkg_factors.get(packaging, 1.0)

    # 6. Storage Condition Environment Factor
    if condition == "Frozen":
        cond_factor = 1.8 if optimal_condition != "Frozen" else 1.0
    elif condition == optimal_condition:
        cond_factor = 1.0
    elif condition == "Room Temperature" and optimal_condition == "Refrigerated":
        cond_factor = 0.40  # Severe penalty for room temp storage of refrigerated perishables
    elif condition == "Controlled Storage":
        cond_factor = 1.15
    else:
        cond_factor = 0.75

    # 7. Historical Degradation Velocity Trend Factor
    if trend == "Declining" and deg_rate is not None and deg_rate > 0:
        trend_factor = max(0.5, 1.0 - (deg_rate * 0.05))
    elif trend == "Improving":
        trend_factor = 1.05
    else:
        trend_factor = 1.0

    # 8. Composite Formula & Remaining Days Calculation
    raw_remaining = (
        base_days * 
        freshness_factor * 
        spoilage_factor * 
        temp_factor * 
        humidity_factor * 
        pkg_factor * 
        cond_factor * 
        trend_factor
    ) - age_days

    # Guarantee non-negative remaining days
    remaining_days = max(0, int(round(raw_remaining)))

    # 9. Estimated Expiry Date (guaranteed consistent with remaining_days)
    estimated_expiry = date.today() + timedelta(days=remaining_days)

    # 10. Operational Risk Level Classification
    if remaining_days == 0 or (has_image_analysis and (spoilage_prob >= 0.70 or freshness_score < 40)):
        risk_level = "CRITICAL"
    elif remaining_days <= 3 or (has_image_analysis and (spoilage_prob >= 0.45 or freshness_score < 60)) or trend == "Declining":
        risk_level = "HIGH RISK"
    elif remaining_days <= 7 or (has_image_analysis and spoilage_prob >= 0.25) or temp_delta > 3.0:
        risk_level = "MEDIUM RISK"
    else:
        risk_level = "LOW RISK"

    # 11. Storage Impact Factors Breakdown & Observations
    storage_impact_observations = []
    if temp_delta > 2.0:
        storage_impact_observations.append(
            f"Storage temperature ({features['storage_temperature']}°C) is {temp_delta}°C higher than optimal ({features['optimal_temperature']}°C), accelerating decay."
        )
    elif temp_delta < -1.0:
        storage_impact_observations.append(
            f"Cold storage temperature ({features['storage_temperature']}°C) provides favorable preservation."
        )

    if humidity_delta > 15.0:
        storage_impact_observations.append(
            f"Relative humidity ({features['storage_humidity']}%) deviates from recommended {features['optimal_humidity']}%, affecting texture."
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
        "freshness_factor": round(freshness_factor, 2),
        "spoilage_factor": round(spoilage_factor, 2),
        "trend_factor": round(trend_factor, 2),
        "observations": storage_impact_observations
    }

    # 12. Contributing Factors
    contributing_factors = {
        "has_image_analysis": has_image_analysis,
        "freshness_score_weight": f"{freshness_score}/100" if has_image_analysis else "N/A (Storage Baseline)",
        "spoilage_probability": f"{spoilage_prob * 100:.1f}%" if has_image_analysis else "N/A (Storage Baseline)",
        "product_age_days": age_days,
        "base_category_shelf_life": f"{base_days} days",
        "historical_trend": trend,
        "degradation_rate_per_day": f"{deg_rate:.2f}/day" if deg_rate is not None else "N/A"
    }

    # 13. Conservative Storage Guidance
    guidance = []
    if risk_level in ["CRITICAL", "HIGH RISK"]:
        guidance.append("Inspect item immediately and prioritize for consumption or retail clearance.")
    if temp_delta > 2.0:
        guidance.append(f"Lower storage temperature closer to optimal {features['optimal_temperature']}°C.")
    if condition == "Room Temperature" and optimal_condition == "Refrigerated":
        guidance.append("Transfer item to refrigerated storage immediately to slow decay.")
    if not guidance:
        guidance.append("Maintain current cold-chain storage conditions and monitor regularly.")

    # 14. Transparent Heuristic Baseline Confidence Calculation
    confidence = 0.30
    if has_image_analysis:
        confidence += 0.30
    if has_storage_log:
        confidence += 0.20
    if sufficient_data:
        confidence += 0.15
    if packaging != "Standard Packaging":
        confidence += 0.05
    
    confidence = round(max(0.30, min(0.95, confidence)), 2)

    return {
        "estimated_remaining_days": remaining_days,
        "estimated_expiry_date": estimated_expiry.isoformat(),
        "risk_level": risk_level,
        "confidence": confidence,
        "trend": trend,
        "degradation_rate_per_day": deg_rate,
        "sufficient_data": sufficient_data,
        "has_image_analysis": has_image_analysis,
        "has_storage_log": has_storage_log,
        "storage_impact": storage_impact,
        "contributing_factors": contributing_factors,
        "storage_guidance": guidance,
        "input_features": features,
        "model_version": MODEL_VERSION
    }
