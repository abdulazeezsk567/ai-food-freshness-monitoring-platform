import pytest
from datetime import date, timedelta

def test_dashboard_stats_extended_analytics(client, retail_token):
    headers = {"Authorization": f"Bearer {retail_token}"}

    # Create food item and inventory batch
    food_res = client.post("/api/food-items", json={
        "name": "Stats Test Strawberries",
        "category": "Fruits",
        "description": "Strawberries for dashboard analytics testing"
    }, headers=headers)
    assert food_res.status_code == 201
    food_id = food_res.json()["id"]

    inv_res = client.post("/api/inventory", json={
        "food_item_id": food_id,
        "batch_number": "BATCH-STATS-01",
        "quantity": 15.0,
        "unit": "kg",
        "purchase_date": str(date.today()),
        "expiry_date": str(date.today() + timedelta(days=5)),
        "storage_temperature": 3.2,
        "storage_humidity": 86.5,
        "packaging_type": "Plastic Tray with Film",
        "storage_duration": 5
    }, headers=headers)
    assert inv_res.status_code == 201
    inv_id = inv_res.json()["id"]

    # Ingest a prediction for this batch
    pred_res = client.post("/api/shelf-life/predict", json={
        "inventory_id": inv_id
    }, headers=headers)
    assert pred_res.status_code == 201

    # Call dashboard stats endpoint
    res = client.get("/api/stats/dashboard", headers=headers)
    assert res.status_code == 200
    data = res.json()

    # Verify standard counts
    assert "total_food_items" in data
    assert "active_batches" in data
    assert data["active_batches"] >= 1

    # Verify Milestone 4 Extended Analytics
    assert "facility_telemetry" in data
    assert data["facility_telemetry"] is not None
    assert "avg_temperature" in data["facility_telemetry"]
    assert "avg_humidity" in data["facility_telemetry"]
    assert isinstance(data["facility_telemetry"]["avg_temperature"], float)
    assert isinstance(data["facility_telemetry"]["avg_humidity"], float)

    # Verify Shelf-Life Analytics
    assert "shelf_life_analytics" in data
    assert data["shelf_life_analytics"] is not None
    assert "risk_distribution" in data["shelf_life_analytics"]
    assert "CRITICAL" in data["shelf_life_analytics"]["risk_distribution"]
    assert "LOW RISK" in data["shelf_life_analytics"]["risk_distribution"]
    assert data["shelf_life_analytics"]["total_predictions"] >= 1

    # Verify Freshness Analytics
    assert "freshness_analytics" in data
    assert data["freshness_analytics"] is not None
    assert "total_analyses" in data["freshness_analytics"]
    assert "avg_freshness_score" in data["freshness_analytics"]

    # Verify Spoilage Alerts list
    assert "spoilage_alerts" in data
    assert isinstance(data["spoilage_alerts"], list)

def test_health_check_endpoint(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["version"] == "4.0.0"

    root_res = client.get("/")
    assert root_res.status_code == 200
    assert root_res.json()["status"] == "online"
