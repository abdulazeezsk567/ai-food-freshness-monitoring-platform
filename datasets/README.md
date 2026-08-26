# Food Freshness Monitoring Platform - Dataset Organization

This directory stores raw and processed datasets required for training future computer vision and machine learning models in Milestone 2 and Milestone 3.

## Folder Structure

```text
datasets/
├── raw/
│   ├── fruits/           # Raw fruit freshness image datasets (fresh & rotten apples, bananas, oranges, etc.)
│   ├── vegetables/       # Raw vegetable quality datasets (fresh & spoiled tomatoes, potatoes, carrots, etc.)
│   ├── food_freshness/   # Multi-class Kaggle food freshness dataset
│   └── food101/          # Food-101 dataset for food category classification (101 categories)
│
├── processed/            # Preprocessed, resized, normalized image arrays and train/val/test split manifests
└── README.md             # Dataset documentation & acquisition guidelines
```

---

## Targeted Dataset Specifications

### 1. Fruits Freshness Dataset
- **Description**: High-resolution images of fresh and rotten fruits including apples, bananas, oranges, strawberries, and grapes.
- **Classes**: `fresh_apple`, `rotten_apple`, `fresh_banana`, `rotten_banana`, `fresh_orange`, `rotten_orange`.
- **Primary Use**: Visual fruit degradation classification & freshness score estimation (0–100%).

### 2. Vegetable Quality Dataset
- **Description**: Images of vegetables at various stages of shelf-life under standard storage conditions.
- **Classes**: `fresh_tomato`, `spoiled_tomato`, `fresh_cucumber`, `spoiled_cucumber`, `fresh_bell_pepper`, `spoiled_bell_pepper`.
- **Primary Use**: Mold/spoilage detection and surface discoloration analysis.

### 3. Kaggle Food Freshness Dataset
- **Description**: Benchmark dataset with environmental metadata and multi-category spoilage labels.
- **Primary Use**: Multi-modal fusion model taking image features + ambient temperature/humidity readings to predict remaining shelf life in days.

### 4. Food-101 Dataset
- **Description**: 101,000 images across 101 food categories.
- **Primary Use**: Automatic food category identification when adding inventory items (`Fruits`, `Vegetables`, `Dairy`, `Bakery`, `Meat`, etc.).

---

## Data Pipeline Plan for Milestone 2 & 3

1. **Ingestion & Data Cleansing**:
   - Extract raw image files into `datasets/raw/<category>/`.
   - Remove corrupted images or invalid metadata.

2. **Preprocessing & Augmentation**:
   - Resize images to $224 \times 224$ or $299 \times 299$ resolution.
   - Standardize pixel normalization ($\mu = [0.485, 0.456, 0.406]$, $\sigma = [0.229, 0.224, 0.225]$).
   - Apply random rotations, horizontal flips, and brightness jitter for data augmentation.

3. **Train/Val/Test Split Manifests**:
   - Save CSV/JSON split manifests in `datasets/processed/` with 80% train, 10% validation, and 10% test ratios.

---
