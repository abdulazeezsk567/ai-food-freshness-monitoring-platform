import os
import json
import numpy as np
from typing import Optional, Any, Dict

_MODEL_CACHE: Optional[Dict[str, Any]] = None
_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "ml", "models", "freshness_model.json")

class ModelWrapper:
    def __init__(self, centroids: Dict[str, list], categories: list):
        self.centroids = centroids
        self.categories = categories

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        probs_list = []
        for x in X:
            dists = np.array([
                np.linalg.norm(x - np.array(self.centroids[cat])) for cat in self.categories
            ])
            logits = -4.0 * dists
            exp_logits = np.exp(logits - np.max(logits))
            probs = exp_logits / np.sum(exp_logits)
            probs_list.append(probs)
        return np.array(probs_list)

def get_trained_model() -> Optional[Any]:
    """
    Singleton model loader caching trained model centroids in memory.
    """
    global _MODEL_CACHE
    if _MODEL_CACHE is not None:
        return _MODEL_CACHE

    model_abs_path = os.path.abspath(_MODEL_PATH)
    if os.path.exists(model_abs_path):
        try:
            with open(model_abs_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            _MODEL_CACHE = ModelWrapper(data["centroids"], data["categories"])
            return _MODEL_CACHE
        except Exception as e:
            print(f"Warning: Failed to load trained model JSON from '{model_abs_path}': {e}")
            return None
    return None
