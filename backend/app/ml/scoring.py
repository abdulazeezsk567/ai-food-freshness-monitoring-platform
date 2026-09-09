from typing import Dict, Any, Tuple

def compute_freshness_score_and_spoilage_prob(
    color_res: Dict[str, Any],
    texture_res: Dict[str, Any],
    spoilage_res: Dict[str, Any],
    probs_dict: Dict[str, float]
) -> Tuple[int, float]:
    """
    Computes a transparent 0-100 Freshness Score and exact Spoilage Probability.
    
    Freshness Score Methodology:
    Freshness Score = max(0, min(100, round(100 * (1 - Composite Spoilage Index))))
    where Composite Spoilage Index combines weighted color degradation, texture roughness,
    browning index, and detected spoilage indicators.
    
    Spoilage Probability Methodology:
    Spoilage Probability = P('Near Spoilage') + P('Spoiled')
    (Distinct from Model Confidence, which measures statistical classification certainty).
    """
    color_degradation = color_res.get("color_degradation_score", 0.0)
    texture_degradation = texture_res.get("texture_score", 0.0)
    browning = color_res.get("browning_index", 0.0) / 100.0
    mold = spoilage_res.get("mold_detection", {}).get("score", 0.0)

    # Composite Spoilage Index (range 0.0 to 1.0)
    composite_spoilage = (
        0.35 * color_degradation +
        0.30 * texture_degradation +
        0.20 * browning +
        0.15 * mold
    )
    composite_spoilage = max(0.0, min(1.0, composite_spoilage))

    # Freshness Score (0 - 100)
    freshness_score = int(round(100.0 * (1.0 - composite_spoilage)))

    # Spoilage Probability = sum of probabilities for 'Near Spoilage' and 'Spoiled'
    p_near_spoilage = probs_dict.get("Near Spoilage", 0.0)
    p_spoiled = probs_dict.get("Spoiled", 0.0)
    spoilage_prob = round(float(min(1.0, p_near_spoilage + p_spoiled)), 4)

    return freshness_score, spoilage_prob
