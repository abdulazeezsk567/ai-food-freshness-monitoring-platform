import cv2
import numpy as np
from typing import Dict, Any

def detect_spoilage_indicators(
    img_rgb: np.ndarray,
    color_res: Dict[str, Any],
    texture_res: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Evaluates specific visual spoilage indicators: Color Degradation, Surface Texture Changes,
    Mold Spot Clusters, Bruising/Soft Spots, and Physical Damage.
    """
    indicators = {}

    # 1. Color Degradation Indicator
    color_score = color_res.get("color_degradation_score", 0.0)
    color_detected = color_score >= 0.35
    indicators["color_degradation"] = {
        "detected": color_detected,
        "score": color_score,
        "evidence": f"Browning index {color_res.get('browning_index', 0)} with {color_res.get('discolored_pixel_ratio', 0)*100:.1f}% surface discoloration."
        if color_detected else "Normal natural color retention observed across sample image."
    }

    # 2. Surface Texture Changes Indicator
    text_score = texture_res.get("texture_score", 0.0)
    texture_detected = text_score >= 0.40
    indicators["surface_texture_changes"] = {
        "detected": texture_detected,
        "score": text_score,
        "evidence": f"Gradient variance ({texture_res.get('gradient_variance', 0):.0f}) indicates surface shriveling or texture breakdown."
        if texture_detected else "Smooth, uniform texture matching un-wilted fresh produce."
    }

    # 3. Mold / Fungal Growth Spot Detection (HSV grayish-white/green spot cluster detection)
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    h, s, v = img_hsv[:, :, 0], img_hsv[:, :, 1], img_hsv[:, :, 2]
    # Mold spots are typically low saturation (s < 40) and high/mid value (v > 150) in localized clusters
    mold_mask = (s < 45) & (v > 160) & (h > 40) & (h < 130)
    mold_pixels = int(np.sum(mold_mask))
    total_pixels = img_rgb.shape[0] * img_rgb.shape[1]
    mold_ratio = round(mold_pixels / float(total_pixels), 4)

    # Perform connected components to find localized mold spot clusters
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mold_mask.astype(np.uint8))
    has_large_cluster = False
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] > (total_pixels * 0.015):
            has_large_cluster = True
            break

    mold_detected = mold_ratio > 0.06 and has_large_cluster
    mold_score = round(min(1.0, mold_ratio * 5.0), 2)
    indicators["mold_detection"] = {
        "detected": mold_detected,
        "score": mold_score,
        "evidence": f"Localized fuzzy mold/fungal spot cluster detected ({mold_ratio*100:.1f}% surface area)."
        if mold_detected else "No significant localized mold or fungal spot clusters detected."
    }

    # 4. Bruising & Soft Spot Risk (Luminance intensity depressions)
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)
    diff = cv2.absdiff(gray, blurred)
    bruise_score = round(float(np.clip(np.mean(diff) / 25.0, 0.0, 1.0)), 2)
    bruise_detected = bruise_score > 0.45
    indicators["bruising_detection"] = {
        "detected": bruise_detected,
        "score": bruise_score,
        "evidence": "Local intensity depression variance suggests soft spot or mechanical bruising."
        if bruise_detected else "Uniform luminance distribution without soft spot depressions."
    }

    # 5. Physical Damage / Cuts
    edges = cv2.Canny(gray, 100, 200)
    edge_density = float(np.sum(edges > 0)) / float(total_pixels)
    damage_score = round(float(np.clip(edge_density * 8.0, 0.0, 1.0)), 2)
    damage_detected = damage_score > 0.4
    indicators["physical_damage"] = {
        "detected": damage_detected,
        "score": damage_score,
        "evidence": "Sharp high-contrast contour edge density indicative of surface puncture or split."
        if damage_detected else "Intact outer surface contour without structural cuts or punctures."
    }

    return indicators
