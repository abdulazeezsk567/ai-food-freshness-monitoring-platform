import cv2
import numpy as np
from typing import Dict, Any, List

def analyze_color(img_rgb: np.ndarray) -> Dict[str, Any]:
    """
    Performs color space conversion (RGB -> HSV & LAB) to evaluate
    browning index, discoloration coverage, and color degradation score.
    """
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)

    # Extract channel statistics
    mean_hsv = [float(np.mean(img_hsv[:, :, i])) for i in range(3)]
    mean_lab = [float(np.mean(img_lab[:, :, i])) for i in range(3)]

    # Browning & Dark Discoloration Detection in HSV (Hue: 0-30 brown/dark, Saturation > 30, Value < 180)
    h, s, v = img_hsv[:, :, 0], img_hsv[:, :, 1], img_hsv[:, :, 2]
    
    # Mask brown/decayed pixels
    brown_mask = ((h <= 28) | (h >= 165)) & (s >= 35) & (v <= 190)
    brown_pixel_count = int(np.sum(brown_mask))
    total_pixels = img_rgb.shape[0] * img_rgb.shape[1]
    discolored_ratio = round(brown_pixel_count / float(total_pixels), 4)

    # LAB Browning Index calculation: BI = 100 * (x - 0.31) / 0.17 where x = (a + 1.75*L) / (5.645*L + a - 3.012*b)
    L, a, b = img_lab[:, :, 0], img_lab[:, :, 1], img_lab[:, :, 2]
    mean_L = np.mean(L) + 1e-5
    mean_a = np.mean(a)
    mean_b = np.mean(b)
    x = (mean_a + 1.75 * mean_L) / (5.645 * mean_L + mean_a - 3.012 * mean_b + 1e-5)
    browning_index = round(float(max(0.0, 100.0 * (x - 0.31) / 0.17)), 2)

    # Normalize color degradation score between 0.0 (Perfect fresh) and 1.0 (Highly degraded)
    degradation_score = round(float(np.clip(discolored_ratio * 2.2 + (browning_index / 120.0) * 0.4, 0.0, 1.0)), 3)

    observations: List[str] = []
    if degradation_score < 0.2:
        status_label = "Optimal Fresh Color"
        observations.append("Vibrant natural pigmentation with minimal surface discoloration.")
        observations.append(f"Discolored area ratio is very low ({discolored_ratio * 100:.1f}%).")
    elif degradation_score < 0.45:
        status_label = "Good Color Quality"
        observations.append("Minor natural hue variations consistent with normal storage.")
        observations.append(f"Discolored region covers approximately {discolored_ratio * 100:.1f}% of surface.")
    elif degradation_score < 0.7:
        status_label = "Moderate Browning / Discoloration"
        observations.append(f"Noticeable browning index detected ({browning_index}).")
        observations.append(f"Surface discoloration coverage is {discolored_ratio * 100:.1f}%.")
    else:
        status_label = "Severe Color Degradation"
        observations.append(f"Extensive dark browning coverage detected ({discolored_ratio * 100:.1f}% of surface).")
        observations.append("Pigment breakdown indicates advanced decay or oxidation.")

    return {
        "color_degradation_score": degradation_score,
        "browning_index": browning_index,
        "discolored_pixel_ratio": discolored_ratio,
        "mean_hsv": [round(val, 1) for val in mean_hsv],
        "mean_lab": [round(val, 1) for val in mean_lab],
        "status": status_label,
        "observations": observations
    }
