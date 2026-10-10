import pytest
import io
import csv
from datetime import date, timedelta

def test_export_inventory_csv(client, retail_token):
    headers = {"Authorization": f"Bearer {retail_token}"}

    # Ensure at least one item exists
    food_res = client.post("/api/food-items", json={
        "name": "Report Export Apple",
        "category": "Fruits",
        "description": "Apples for CSV export testing"
    }, headers=headers)
    food_id = food_res.json()["id"]

    client.post("/api/inventory", json={
        "food_item_id": food_id,
        "batch_number": "BATCH-CSV-01",
        "quantity": 50.0,
        "unit": "kg",
        "purchase_date": str(date.today()),
        "expiry_date": str(date.today() + timedelta(days=10)),
        "storage_temperature": 3.5,
        "storage_humidity": 88.0,
        "packaging_type": "Standard Packaging",
        "storage_duration": 10
    }, headers=headers)

    res = client.get("/api/reports/inventory/csv", headers=headers)
    assert res.status_code == 200
    assert "text/csv" in res.headers["content-type"]
    assert "attachment; filename=" in res.headers["content-disposition"]

    # Verify CSV content structure
    content = res.text
    reader = csv.reader(io.StringIO(content))
    rows = list(reader)
    assert len(rows) >= 2  # At least header + 1 data row
    header = rows[0]
    assert "Batch Number" in header
    assert "Food Item" in header
    assert "Expiry Date" in header
    assert "Freshness Status" in header

def test_export_shelf_life_report_json(client, retail_token):
    headers = {"Authorization": f"Bearer {retail_token}"}

    # Create batch and prediction
    food_res = client.post("/api/food-items", json={
        "name": "Report Export Yogurt",
        "category": "Dairy Products",
        "description": "Yogurt for shelf-life report export"
    }, headers=headers)
    food_id = food_res.json()["id"]

    inv_res = client.post("/api/inventory", json={
        "food_item_id": food_id,
        "batch_number": "BATCH-SLP-REP-01",
        "quantity": 20.0,
        "unit": "liters",
        "purchase_date": str(date.today()),
        "expiry_date": str(date.today() + timedelta(days=7)),
        "storage_temperature": 2.5,
        "storage_humidity": 80.0,
        "packaging_type": "Standard Packaging",
        "storage_duration": 7
    }, headers=headers)
    inv_id = inv_res.json()["id"]

    pred_res = client.post("/api/shelf-life/predict", json={
        "inventory_id": inv_id
    }, headers=headers)
    pred_id = pred_res.json()["id"]

    # Export report JSON
    rep_res = client.get(f"/api/reports/shelf-life/{pred_id}/json", headers=headers)
    assert rep_res.status_code == 200
    assert "application/json" in rep_res.headers["content-type"]
    assert f"attachment; filename=\"shelf_life_prediction_report_{pred_id}.json\"" in rep_res.headers["content-disposition"]

    data = rep_res.json()
    assert "metadata" in data
    assert data["metadata"]["report_type"] == "Predictive Shelf-Life Forecast Report"
    assert "shelf-life-baseline-v1" in data["metadata"]["model_architecture"]
    assert "forecast_data" in data
    assert data["forecast_data"]["prediction_id"] == pred_id
    assert "estimated_remaining_days" in data["forecast_data"]
    assert "risk_level" in data["forecast_data"]

def test_export_report_404(client, retail_token):
    headers = {"Authorization": f"Bearer {retail_token}"}
    res = client.get("/api/reports/shelf-life/999999/json", headers=headers)
    assert res.status_code == 404
    res_fresh = client.get("/api/reports/freshness/999999/json", headers=headers)
    assert res_fresh.status_code == 404
