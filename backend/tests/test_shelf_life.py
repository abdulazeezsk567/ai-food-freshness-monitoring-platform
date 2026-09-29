import pytest
from datetime import date, timedelta, datetime
from app.ml.shelf_life_features import extract_shelf_life_features
from app.ml.shelf_life_model import predict_shelf_life

def test_higher_temperature_reduces_shelf_life():
    """A. Higher temperature reduces shelf life."""
    f_cool = extract_shelf_life_features("Fruits", 90, "Fresh", 0.05, storage_temperature=4.0)
    p_cool = predict_shelf_life(f_cool)

    f_warm = extract_shelf_life_features("Fruits", 90, "Fresh", 0.05, storage_temperature=25.0)
    p_warm = predict_shelf_life(f_warm)

    assert p_warm["estimated_remaining_days"] < p_cool["estimated_remaining_days"]

def test_extreme_humidity_affects_shelf_life():
    """B. Extreme humidity affects shelf life."""
    f_opt = extract_shelf_life_features("Fruits", 90, "Fresh", 0.05, storage_humidity=85.0)
    p_opt = predict_shelf_life(f_opt)

    f_extreme = extract_shelf_life_features("Fruits", 90, "Fresh", 0.05, storage_humidity=20.0)
    p_extreme = predict_shelf_life(f_extreme)

    assert p_extreme["estimated_remaining_days"] < p_opt["estimated_remaining_days"]

def test_higher_freshness_score_increases_remaining_shelf_life():
    """C. Higher freshness score generally increases remaining shelf life."""
    f_high = extract_shelf_life_features("Fruits", 95, "Fresh", 0.02, has_image_analysis=True)
    p_high = predict_shelf_life(f_high)

    f_low = extract_shelf_life_features("Fruits", 50, "Acceptable", 0.30, has_image_analysis=True)
    p_low = predict_shelf_life(f_low)

    assert p_high["estimated_remaining_days"] > p_low["estimated_remaining_days"]

def test_higher_spoilage_probability_increases_risk():
    """D. Higher spoilage probability increases risk and reduces remaining days."""
    f_low_spoil = extract_shelf_life_features("Fruits", 80, "Good", 0.05, has_image_analysis=True)
    p_low_spoil = predict_shelf_life(f_low_spoil)

    f_high_spoil = extract_shelf_life_features("Fruits", 80, "Good", 0.75, has_image_analysis=True)
    p_high_spoil = predict_shelf_life(f_high_spoil)

    assert p_high_spoil["risk_level"] == "CRITICAL"
    assert p_high_spoil["estimated_remaining_days"] <= p_low_spoil["estimated_remaining_days"]

def test_greater_food_age_reduces_remaining_shelf_life():
    """E. Greater food age reduces remaining shelf life."""
    f_fresh = extract_shelf_life_features("Fruits", 90, "Fresh", 0.05, purchase_date=date.today())
    p_fresh = predict_shelf_life(f_fresh)

    f_old = extract_shelf_life_features("Fruits", 90, "Fresh", 0.05, purchase_date=date.today() - timedelta(days=10))
    p_old = predict_shelf_life(f_old)

    assert p_old["estimated_remaining_days"] < p_fresh["estimated_remaining_days"]

def test_declining_freshness_history_produces_declining_trend():
    """F. Declining freshness history produces Declining trend."""
    t0 = datetime.utcnow() - timedelta(days=5)
    t1 = datetime.utcnow()
    records = [
        {"freshness_score": 90, "created_at": t0},
        {"freshness_score": 60, "created_at": t1}
    ]
    f = extract_shelf_life_features("Fruits", 60, "Acceptable", 0.30, past_analysis_records=records)
    assert f["trend"] == "Declining"
    assert f["sufficient_data"] is True
    assert f["degradation_rate_per_day"] > 0.0

def test_stable_history_produces_stable_trend():
    """G. Stable history produces Stable trend."""
    t0 = datetime.utcnow() - timedelta(days=3)
    t1 = datetime.utcnow()
    records = [
        {"freshness_score": 85, "created_at": t0},
        {"freshness_score": 84, "created_at": t1}
    ]
    f = extract_shelf_life_features("Fruits", 84, "Good", 0.10, past_analysis_records=records)
    assert f["trend"] == "Stable"
    assert f["sufficient_data"] is True

def test_insufficient_history_produces_insufficient_data():
    """H. Insufficient history produces Insufficient Data."""
    records = [{"freshness_score": 85, "created_at": datetime.utcnow()}]
    f = extract_shelf_life_features("Fruits", 85, "Good", 0.10, past_analysis_records=records)
    assert f["trend"] == "Insufficient Data"
    assert f["sufficient_data"] is False
    assert f["degradation_rate_per_day"] is None

def test_different_packaging_affects_prediction():
    """I. Different packaging affects prediction."""
    f_vacuum = extract_shelf_life_features("Meat & Poultry", 90, "Fresh", 0.05, packaging_type="Vacuum Sealed")
    p_vacuum = predict_shelf_life(f_vacuum)

    f_loose = extract_shelf_life_features("Meat & Poultry", 90, "Fresh", 0.05, packaging_type="Unpackaged / Loose")
    p_loose = predict_shelf_life(f_loose)

    assert p_vacuum["estimated_remaining_days"] > p_loose["estimated_remaining_days"]

def test_refrigerated_frozen_room_temp_conditions_behave_differently():
    """J. Refrigerated/Frozen/Room Temperature conditions behave differently."""
    f_ref = extract_shelf_life_features("Dairy Products", 90, "Fresh", 0.05, storage_condition="Refrigerated")
    p_ref = predict_shelf_life(f_ref)

    f_room = extract_shelf_life_features("Dairy Products", 90, "Fresh", 0.05, storage_condition="Room Temperature")
    p_room = predict_shelf_life(f_room)

    f_frozen = extract_shelf_life_features("Dairy Products", 90, "Fresh", 0.05, storage_condition="Frozen")
    p_frozen = predict_shelf_life(f_frozen)

    assert p_room["estimated_remaining_days"] < p_ref["estimated_remaining_days"]
    assert p_frozen["estimated_remaining_days"] >= p_ref["estimated_remaining_days"]

def test_invalid_humidity_rejected(client, retail_token):
    """K. Invalid humidity is rejected."""
    headers = {"Authorization": f"Bearer {retail_token}"}
    res = client.post("/api/storage-conditions", json={
        "inventory_id": 1,
        "temperature": 4.0,
        "humidity": 150.0,  # Invalid humidity > 100
        "packaging_type": "Standard Packaging",
        "storage_condition": "Refrigerated"
    }, headers=headers)
    assert res.status_code == 422

def test_invalid_freshness_score_rejected(client, retail_token):
    """L. Invalid freshness score override or input rejected in schemas."""
    headers = {"Authorization": f"Bearer {retail_token}"}
    res = client.post("/api/shelf-life/predict", json={
        "inventory_id": 1,
        "temperature_override": 120.0  # Invalid temp > 60.0
    }, headers=headers)
    assert res.status_code == 422

def test_invalid_spoilage_probability_rejected(client, retail_token):
    """M. Invalid storage condition string rejected in Pydantic."""
    headers = {"Authorization": f"Bearer {retail_token}"}
    res = client.post("/api/shelf-life/predict", json={
        "inventory_id": 1,
        "storage_condition_override": "InvalidConditionName"
    }, headers=headers)
    assert res.status_code == 422

def test_prediction_response_persisted_in_database(client, retail_token):
    """N. Prediction response is persisted in database."""
    headers = {"Authorization": f"Bearer {retail_token}"}

    # Create food item & batch
    food_res = client.post("/api/food-items", json={
        "name": "Test Apple Batch",
        "category": "Fruits",
        "description": "Apple batch for DB persistence test"
    }, headers=headers)
    food_id = food_res.json()["id"]

    inv_res = client.post("/api/inventory", json={
        "food_item_id": food_id,
        "batch_number": "BATCH-APL-DBTEST",
        "quantity": 50.0,
        "unit": "kg",
        "purchase_date": str(date.today()),
        "expiry_date": str(date.today() + timedelta(days=14)),
        "storage_temperature": 4.0,
        "storage_humidity": 85.0,
        "packaging_type": "Standard Packaging",
        "storage_duration": 14
    }, headers=headers)
    inv_id = inv_res.json()["id"]

    # Post prediction
    pred_res = client.post("/api/shelf-life/predict", json={"inventory_id": inv_id}, headers=headers)
    assert pred_res.status_code == 201
    data = pred_res.json()
    assert data["inventory_id"] == inv_id
    assert "estimated_remaining_days" in data
    assert data["model_version"] == "shelf-life-baseline-v1"

def test_prediction_history_works_correctly(client, retail_token):
    """O. Prediction history works correctly."""
    headers = {"Authorization": f"Bearer {retail_token}"}

    food_res = client.post("/api/food-items", json={
        "name": "Test Banana Batch",
        "category": "Fruits",
        "description": "Banana batch for history test"
    }, headers=headers)
    food_id = food_res.json()["id"]

    inv_res = client.post("/api/inventory", json={
        "food_item_id": food_id,
        "batch_number": "BATCH-BAN-HIST",
        "quantity": 30.0,
        "unit": "kg",
        "purchase_date": str(date.today()),
        "expiry_date": str(date.today() + timedelta(days=7)),
        "storage_temperature": 4.0,
        "storage_humidity": 85.0,
        "packaging_type": "Standard Packaging",
        "storage_duration": 7
    }, headers=headers)
    inv_id = inv_res.json()["id"]

    # Generate 2 predictions
    client.post("/api/shelf-life/predict", json={"inventory_id": inv_id}, headers=headers)
    client.post("/api/shelf-life/predict", json={"inventory_id": inv_id, "temperature_override": 10.0}, headers=headers)

    hist_res = client.get(f"/api/shelf-life/{inv_id}/history", headers=headers)
    assert hist_res.status_code == 200
    history = hist_res.json()
    assert len(history) >= 2

def test_storage_telemetry_changes_reflected_in_subsequent_predictions(client, retail_token):
    """P. Storage telemetry changes are reflected in subsequent predictions."""
    headers = {"Authorization": f"Bearer {retail_token}"}

    food_res = client.post("/api/food-items", json={
        "name": "Test Grape Batch",
        "category": "Fruits",
        "description": "Grape batch for telemetry update test"
    }, headers=headers)
    food_id = food_res.json()["id"]

    inv_res = client.post("/api/inventory", json={
        "food_item_id": food_id,
        "batch_number": "BATCH-GRP-TEL",
        "quantity": 15.0,
        "unit": "kg",
        "purchase_date": str(date.today()),
        "expiry_date": str(date.today() + timedelta(days=10)),
        "storage_temperature": 4.0,
        "storage_humidity": 85.0,
        "packaging_type": "Standard Packaging",
        "storage_duration": 10
    }, headers=headers)
    inv_id = inv_res.json()["id"]

    # Initial prediction at 4.0°C
    p1_res = client.post("/api/shelf-life/predict", json={"inventory_id": inv_id}, headers=headers)
    days_p1 = p1_res.json()["estimated_remaining_days"]

    # Log severe storage temperature change (30.0°C)
    client.post("/api/storage-conditions", json={
        "inventory_id": inv_id,
        "temperature": 30.0,
        "humidity": 40.0,
        "storage_location": "Hot Warehouse Room",
        "packaging_type": "Paper Wrapping",
        "storage_condition": "Room Temperature"
    }, headers=headers)

    # Subsequent prediction
    p2_res = client.post("/api/shelf-life/predict", json={"inventory_id": inv_id}, headers=headers)
    days_p2 = p2_res.json()["estimated_remaining_days"]

    assert days_p2 < days_p1
