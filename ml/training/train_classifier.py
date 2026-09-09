import os
import json
import numpy as np
from typing import Tuple, Dict, Any

CATEGORIES = ["Fresh", "Good", "Acceptable", "Near Spoilage", "Spoiled"]

class BaselineFreshnessClassifier:
    def __init__(self):
        self.centroids = {}
        self.category_names = CATEGORIES

    def fit(self, X: np.ndarray, y: np.ndarray):
        for idx, cat in enumerate(self.category_names):
            class_samples = X[y == idx]
            if len(class_samples) > 0:
                self.centroids[idx] = np.mean(class_samples, axis=0)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        probs_list = []
        for x in X:
            dists = np.array([np.linalg.norm(x - self.centroids[i]) for i in range(len(self.category_names))])
            logits = -4.0 * dists
            exp_logits = np.exp(logits - np.max(logits))
            probs = exp_logits / np.sum(exp_logits)
            probs_list.append(probs)
        return np.array(probs_list)

    def predict(self, X: np.ndarray) -> np.ndarray:
        probs = self.predict_proba(X)
        return np.argmax(probs, axis=1)

def generate_synthetic_feature_dataset(samples_per_class: int = 200) -> Tuple[np.ndarray, np.ndarray]:
    np.random.seed(42)
    X_list = []
    y_list = []

    # Category 0: Fresh
    f_fresh = np.column_stack([
        np.random.uniform(0.0, 0.18, samples_per_class),   # color
        np.random.uniform(0.0, 0.22, samples_per_class),   # texture
        np.random.uniform(0.0, 0.15, samples_per_class),   # browning
        np.random.uniform(0.0, 0.05, samples_per_class)    # mold
    ])
    X_list.append(f_fresh)
    y_list.append(np.zeros(samples_per_class, dtype=int))

    # Category 1: Good
    f_good = np.column_stack([
        np.random.uniform(0.15, 0.35, samples_per_class),
        np.random.uniform(0.18, 0.40, samples_per_class),
        np.random.uniform(0.10, 0.32, samples_per_class),
        np.random.uniform(0.0, 0.08, samples_per_class)
    ])
    X_list.append(f_good)
    y_list.append(np.ones(samples_per_class, dtype=int))

    # Category 2: Acceptable
    f_acc = np.column_stack([
        np.random.uniform(0.32, 0.55, samples_per_class),
        np.random.uniform(0.35, 0.60, samples_per_class),
        np.random.uniform(0.28, 0.52, samples_per_class),
        np.random.uniform(0.02, 0.15, samples_per_class)
    ])
    X_list.append(f_acc)
    y_list.append(np.full(samples_per_class, 2, dtype=int))

    # Category 3: Near Spoilage
    f_near = np.column_stack([
        np.random.uniform(0.52, 0.78, samples_per_class),
        np.random.uniform(0.55, 0.80, samples_per_class),
        np.random.uniform(0.48, 0.75, samples_per_class),
        np.random.uniform(0.10, 0.35, samples_per_class)
    ])
    X_list.append(f_near)
    y_list.append(np.full(samples_per_class, 3, dtype=int))

    # Category 4: Spoiled
    f_spoil = np.column_stack([
        np.random.uniform(0.72, 1.0, samples_per_class),
        np.random.uniform(0.75, 1.0, samples_per_class),
        np.random.uniform(0.70, 1.0, samples_per_class),
        np.random.uniform(0.30, 1.0, samples_per_class)
    ])
    X_list.append(f_spoil)
    y_list.append(np.full(samples_per_class, 4, dtype=int))

    X = np.vstack(X_list)
    y = np.concatenate(y_list)
    return X, y

def train_and_evaluate():
    print("Generating baseline feature dataset...")
    X, y = generate_synthetic_feature_dataset(samples_per_class=300)

    # 80% Train, 10% Val, 10% Test
    n_total = len(X)
    indices = np.random.permutation(n_total)
    train_end = int(0.80 * n_total)
    val_end = int(0.90 * n_total)

    train_idx = indices[:train_end]
    val_idx = indices[train_end:val_end]
    test_idx = indices[val_end:]

    X_train, y_train = X[train_idx], y[train_idx]
    X_val, y_val = X[val_idx], y[val_idx]
    X_test, y_test = X[test_idx], y[test_idx]

    print(f"Dataset split: Train={len(X_train)}, Val={len(X_val)}, Test={len(X_test)}")

    model = BaselineFreshnessClassifier()
    model.fit(X_train, y_train)

    val_preds = model.predict(X_val)
    val_acc = float(np.mean(val_preds == y_val))

    test_preds = model.predict(X_test)
    test_acc = float(np.mean(test_preds == y_test))

    # Confusion matrix
    cm = np.zeros((5, 5), dtype=int)
    for true_lbl, pred_lbl in zip(y_test, test_preds):
        cm[true_lbl, pred_lbl] += 1

    print(f"Validation Accuracy: {val_acc * 100:.2f}%")
    print(f"Test Accuracy: {test_acc * 100:.2f}%")

    # Save model artifact as JSON / Joblib dictionary
    models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))
    os.makedirs(models_dir, exist_ok=True)
    model_json_path = os.path.join(models_dir, "freshness_model.json")
    
    saved_weights = {
        "centroids": {cat: model.centroids[idx].tolist() for idx, cat in enumerate(CATEGORIES)},
        "categories": CATEGORIES
    }
    with open(model_json_path, "w", encoding="utf-8") as f:
        json.dump(saved_weights, f, indent=2)

    print(f"Trained model saved to: {model_json_path}")

    # Generate Evaluation Report Markdown
    eval_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "evaluation"))
    os.makedirs(eval_dir, exist_ok=True)
    report_path = os.path.join(eval_dir, "eval_report.md")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# ML Baseline Model Evaluation Report\n\n")
        f.write("## Model Overview\n")
        f.write("- **Algorithm**: Nearest Centroid & Softmax Probability Mapper\n")
        f.write("- **Target Classes**: `Fresh`, `Good`, `Acceptable`, `Near Spoilage`, `Spoiled`\n")
        f.write("- **Feature Inputs**: `color_degradation_score`, `texture_degradation_score`, `browning_index`, `mold_score`\n\n")
        f.write("## Performance Metrics\n")
        f.write(f"- **Validation Accuracy**: {val_acc * 100:.2f}%\n")
        f.write(f"- **Test Accuracy**: {test_acc * 100:.2f}%\n\n")
        f.write("## Confusion Matrix\n```text\n")
        f.write(str(cm))
        f.write("\n```\n")

    print(f"Evaluation report written to: {report_path}")

if __name__ == "__main__":
    train_and_evaluate()
