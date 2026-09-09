# ML Baseline Model Evaluation Report

## Model Overview
- **Algorithm**: Nearest Centroid & Softmax Probability Mapper
- **Target Classes**: `Fresh`, `Good`, `Acceptable`, `Near Spoilage`, `Spoiled`
- **Feature Inputs**: `color_degradation_score`, `texture_degradation_score`, `browning_index`, `mold_score`

## Performance Metrics
- **Validation Accuracy**: 98.67%
- **Test Accuracy**: 97.33%

## Confusion Matrix
```text
[[25  0  0  0  0]
 [ 1 29  1  0  0]
 [ 0  0 36  0  0]
 [ 0  0  0 33  0]
 [ 0  0  0  2 23]]
```
