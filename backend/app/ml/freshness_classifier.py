import numpy as np
from typing import Dict, Any, List, Tuple

CATEGORIES = ["Fresh", "Good", "Acceptable", "Near Spoilage", "Spoiled"]

def classify_freshness(
    color_res: Dict[str, Any],
    texture_res: Dict[str, Any],
    spoilage_res: Dict[str, Any],
    trained_model: Any = None
) -> Tuple[str, Dict[str, float], float]:
    """
    Classifies food item freshness into 5 categories based on color, texture,
    and spoilage features. Returns (predicted_category, probability_distribution, confidence).
    """
    color_score = color_res.get("color_degradation_score", 0.0)
    texture_score = texture_res.get("texture_score", 0.0)
    browning_index = color_res.get("browning_index", 0.0) / 100.0
    mold_score = spoilage_res.get("mold_detection", {}).get("score", 0.0)

    # Feature vector for ML model inference
    features = np.array([[color_score, texture_score, browning_index, mold_score]], dtype=float)

    if trained_model is not None:
        try:
            probs = trained_model.predict_proba(features)[0]
            probs_dict = {cat: round(float(p), 4) for cat, p in zip(CATEGORIES, probs)}
            best_idx = int(np.argmax(probs))
            predicted_cat = CATEGORIES[best_idx]
            confidence = round(float(probs[best_idx]), 4)
            return predicted_cat, probs_dict, confidence
        except Exception:
            pass  # Fallback to feature-based rule engine

    # Combined Composite Spoilage Index (0.0 = completely fresh, 1.0 = completely spoiled)
    spoilage_index = 0.40 * color_score + 0.30 * texture_score + 0.20 * browning_index + 0.10 * mold_score

    # Distance-based Softmax Probabilities across categories
    # Center points for categories: Fresh(0.05), Good(0.25), Acceptable(0.48), Near Spoilage(0.72), Spoiled(0.92)
    centers = np.array([0.05, 0.25, 0.48, 0.72, 0.92])
    distances = np.abs(spoilage_index - centers)
    logits = -6.0 * distances
    exp_logits = np.exp(logits - np.max(logits))
    probs = exp_logits / np.sum(exp_logits)

    probs_dict = {cat: round(float(p), 4) for cat, p in zip(CATEGORIES, probs)}
    best_idx = int(np.argmax(probs))
    predicted_cat = CATEGORIES[best_idx]
    confidence = round(float(probs[best_idx]), 4)

    return predicted_cat, probs_dict, confidence
