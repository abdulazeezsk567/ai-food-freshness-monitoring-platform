import pytest
from datetime import date, timedelta
from app.ml.shelf_life_features import extract_shelf_life_features
from app.ml.shelf_life_model import predict_shelf_life

def test_feature_extraction_defaults():
    features = extract_shelf_life_features(
        food_category="Fruits",
        freshness_score=85,
        freshness_category="Good",
        spoilage_probability=0.05,
        purchase_date=date.today() - timedelta(days=2),
        storage_temperature=4.0,
        storage_humidity=85.0
    )
    assert features["food_category"] == "Fruits"
    assert features["base_shelf_life_days"] == 14
    assert features["age_days"] == 2
    assert features["trend"] == "Insufficient Data"

def test_prediction_formula_low_risk():
    features = extract_shelf_life_features(
        food_category="Fruits",
        freshness_score=90,
        freshness_category="Fresh",
        spoilage_probability=0.02,
        purchase_date=date.today(),
        storage_temperature=4.0,
        storage_humidity=85.0,
        packaging_type="Standard Packaging",
        storage_condition="Refrigerated"
    )
    prediction = predict_shelf_life(features)
    assert prediction["estimated_remaining_days"] >= 10
    assert prediction["risk_level"] == "LOW RISK"
    assert "shelf-life-baseline-v1" in prediction["model_version"]

def test_prediction_formula_critical_risk():
    features = extract_shelf_life_features(
        food_category="Meat & Poultry",
        freshness_score=35,
        freshness_category="Near Spoilage",
        spoilage_probability=0.75,
        purchase_date=date.today() - timedelta(days=4),
        storage_temperature=12.0,  # High temperature penalty
        storage_condition="Room Temperature"  # Non-refrigerated penalty
    )
    prediction = predict_shelf_life(features)
    assert prediction["estimated_remaining_days"] <= 1
    assert prediction["risk_level"] == "CRITICAL"

def test_degradation_trend_calculation():
    # Insufficient history (<2 scores)
    f_empty = extract_shelf_life_features("Fruits", 80, "Good", 0.10, historical_scores=[80])
    assert f_empty["trend"] == "Insufficient Data"

    # Declining trend
    f_declining = extract_shelf_life_features("Fruits", 60, "Acceptable", 0.30, historical_scores=[92, 80, 60])
    assert f_declining["trend"] == "Declining"

    # Improving trend
    f_improving = extract_shelf_life_features("Fruits", 90, "Fresh", 0.02, historical_scores=[75, 82, 90])
    assert f_improving["trend"] == "Improving"

def test_record_storage_condition_api(client, retail_token):
    headers = {"Authorization": f"Bearer {retail_token}"}
    
    # 1. Create a food item and batch
    food_res = client.post("/api/food-items", json={
        "name": "Test Milk Batch",
        "category": "Dairy Products",
        "description": "Milk batch for storage telemetry test"
    }, headers=headers)
    food_id = food_res.json()["id"]

    inv_res = client.post("/api/inventory", json={
        "food_item_id": food_id,
        "batch_number": "BATCH-MLK-TEST",
        "quantity": 10.0,
        "unit": "liters",
        "purchase_date": str(date.today()),
        "expiry_date": str(date.today() + timedelta(days=7)),
        "storage_temperature": 3.0,
        "storage_humidity": 80.0,
        "packaging_type": "Standard Packaging",
        "storage_duration": 7
    }, headers=headers)
    inv_id = inv_res.json()["id"]

    # 2. Record storage condition log
    storage_res = client.post("/api/storage-conditions", json={
        "inventory_id": inv_id,
        "temperature": 2.5,
        "humidity": 82.0,
        "storage_location": "Cold Vault 2",
        "packaging_type": "Aseptic Packaging",
        "storage_condition": "Refrigerated",
        "storage_duration_days": 3,
        "notes": "Optimal cold chain maintained"
    }, headers=headers)
    assert storage_res.status_code == 201
    s_data = storage_res.json()
    assert s_data["inventory_id"] == inv_id
    assert s_data["temperature"] == 2.5

    # 3. Retrieve latest storage condition log
    get_res = client.get(f"/api/storage-conditions/{inv_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["temperature"] == 2.5

def test_predict_shelf_life_api(client, retail_token):
    headers = {"Authorization": f"Bearer {retail_token}"}

    food_res = client.post("/api/food-items", json={
        "name": "Test Orange Batch",
        "category": "Fruits",
        "description": "Orange batch for predictive shelf-life test"
    }, headers=headers)
    food_id = food_res.json()["id"]

    inv_res = client.post("/api/inventory", json={
        "food_item_id": food_id,
        "batch_number": "BATCH-ORG-TEST",
        "quantity": 25.0,
        "unit": "kg",
        "purchase_date": str(date.today()),
        "expiry_date": str(date.today() + timedelta(days=14)),
        "storage_temperature": 4.0,
        "storage_humidity": 85.0,
        "packaging_type": "Standard Packaging",
        "storage_duration": 14
    }, headers=headers)
    inv_id = inv_res.json()["id"]

    # Request prediction
    pred_res = client.post("/api/shelf-life/predict", json={
        "inventory_id": inv_id
    }, headers=headers)

    assert pred_res.status_code == 201
    p = pred_res.json()
    assert p["inventory_id"] == inv_id
    assert p["estimated_remaining_days"] >= 0
    assert p["risk_level"] in ["LOW RISK", "MEDIUM RISK", "HIGH RISK", "CRITICAL"]
    assert "shelf-life-baseline-v1" in p["model_version"]

    # Retrieve latest prediction via GET
    get_res = client.get(f"/api/shelf-life/{inv_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["inventory_id"] == inv_id
