import os
import io
import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Dict, Any, Optional

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

def validate_image_file(file_path: str, file_size: Optional[int] = None) -> None:
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file format '{ext}'. Allowed formats: JPG, JPEG, PNG, WEBP.")

    if file_size and file_size > MAX_FILE_SIZE_BYTES:
        raise ValueError(f"File size exceeds maximum limit of 10MB ({file_size / (1024*1024):.2f}MB provided).")

    if not os.path.exists(file_path):
        raise ValueError("Image file does not exist on disk.")

def load_and_preprocess_image(
    image_path: str,
    target_size: Tuple[int, int] = (256, 256)
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Loads an image file, converts to RGB NumPy array, resizes to target shape,
    and performs basic image quality & sharpness validation via Laplacian variance.
    """
    validate_image_file(image_path, os.path.getsize(image_path))

    # Read image using OpenCV
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        raise ValueError("Corrupted or unreadable image file. Unable to decode visual pixels.")

    # Convert to RGB
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    height, width, channels = img_rgb.shape

    # Quality check: Laplacian Variance for blur detection
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    is_blurry = blur_score < 40.0

    # Resize image
    resized_rgb = cv2.resize(img_rgb, target_size, interpolation=cv2.INTER_AREA)

    metadata = {
        "original_width": width,
        "original_height": height,
        "channels": channels,
        "blur_score": round(blur_score, 2),
        "is_blurry": is_blurry,
        "target_size": target_size
    }

    return resized_rgb, metadata
