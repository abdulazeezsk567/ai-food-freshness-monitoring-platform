from datetime import datetime
from typing import Dict, Any, Optional

from app.ml.preprocessing import load_and_preprocess_image
from app.ml.color_analysis import analyze_color
from app.ml.texture_analysis import analyze_texture
from app.ml.spoilage_detector import detect_spoilage_indicators
from app.ml.freshness_classifier import classify_freshness
from app.ml.scoring import compute_freshness_score_and_spoilage_prob
from app.ml.model_loader import get_trained_model

MODEL_VERSION = "v1.0.0-CV"

def run_freshness_pipeline(image_path: str, food_category: str = "Fruits") -> Dict[str, Any]:
    """
    Executes the full Milestone 2 image analysis pipeline:
    Image Validation -> Preprocessing -> Color Analysis -> Texture Analysis ->
    Spoilage Indicator Detection -> Freshness Classification -> Scoring -> Analysis Report.
    """
    # 1. Preprocessing & Quality Validation
    img_rgb, prep_meta = load_and_preprocess_image(image_path)

    # 2. Color Analysis
    color_res = analyze_color(img_rgb)

    # 3. Texture Analysis
    texture_res = analyze_texture(img_rgb)

    # 4. Spoilage Indicator Detection
    spoilage_res = detect_spoilage_indicators(img_rgb, color_res, texture_res)

    # 5. Model Loading & Freshness Classification
    trained_model = get_trained_model()
    predicted_cat, probs_dict, confidence = classify_freshness(
        color_res, texture_res, spoilage_res, trained_model
    )

    # 6. Scoring & Spoilage Probability Calculation
    freshness_score, spoilage_prob = compute_freshness_score_and_spoilage_prob(
        color_res, texture_res, spoilage_res, probs_dict
    )

    # 7. Package Full Analysis Report Payload
    report = {
        "analysis_timestamp": datetime.utcnow().isoformat() + "Z",
        "food_category": food_category,
        "predicted_category": predicted_cat,
        "freshness_score": freshness_score,
        "spoilage_probability": spoilage_prob,
        "confidence": confidence,
        "category_probabilities": probs_dict,
        "color_analysis": color_res,
        "texture_analysis": texture_res,
        "spoilage_indicators": spoilage_res,
        "preprocessing_metadata": prep_meta,
        "model_version": MODEL_VERSION
    }

    return report
