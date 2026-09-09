import cv2
import numpy as np
from typing import Dict, Any, List

def analyze_texture(img_rgb: np.ndarray) -> Dict[str, Any]:
    """
    Analyzes visual texture statistics (Laplacian variance, local intensity gradients,
    roughness, and surface irregularity) to estimate structural decay.
    """
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    # 1. Edge Density & Gradient Variance (Sobel Gradients)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(sobelx**2 + sobely**2)
    mean_gradient = float(np.mean(gradient_magnitude))
    gradient_var = float(np.var(gradient_magnitude))

    # 2. Local Intensity Contrast / Roughness
    std_dev = float(np.std(gray))
    laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())

    # 3. Simple GLCM-inspired local homogeneity approximation
    gray_shifted = np.roll(gray, shift=1, axis=1)
    diff = np.abs(gray.astype(float) - gray_shifted.astype(float))
    homogeneity = float(np.mean(1.0 / (1.0 + diff)))

    # Compute texture degradation score (high roughness/heterogeneity = wilting/decay)
    texture_score = round(float(np.clip((gradient_var / 2500.0) * 0.4 + (1.0 - homogeneity) * 0.6, 0.0, 1.0)), 3)

    observations: List[str] = []
    if texture_score < 0.25:
        observations.append("Smooth and uniform skin/surface texture.")
        observations.append("High local homogeneity indicates firm, un-wilted structure.")
    elif texture_score < 0.55:
        observations.append("Moderate texture variation within normal organic limits.")
        observations.append("Slight surface roughness detected, typical of natural produce.")
    else:
        observations.append("Significant surface irregularity and high gradient variance.")
        observations.append("Increased micro-contrast consistent with wilting, shriveling, or structural collapse.")

    return {
        "texture_score": texture_score,
        "homogeneity": round(homogeneity, 4),
        "mean_gradient": round(mean_gradient, 2),
        "gradient_variance": round(gradient_var, 2),
        "laplacian_variance": round(laplacian_var, 2),
        "observations": observations
    }
