import pytest
from datetime import date, timedelta

def test_batch_telemetry_ingestion_success(client, retail_token):
    headers = {"Authorization": f"Bearer {retail_token}"}

    # Create batch
    food_res = client.post("/api/food-items", json={
        "name": "IoT Monitored Chicken",
        "category": "Meat & Poultry",
        "description": "Chicken breast with IoT cold-chain sensor"
    }, headers=headers)
    food_id = food_res.json()["id"]

    inv_res = client.post("/api/inventory", json={
        "food_item_id": food_id,
        "batch_number": "BATCH-IOT-01",
        "quantity": 30.0,
        "unit": "kg",
        "purchase_date": str(date.today()),
        "expiry_date": str(date.today() + timedelta(days=5)),
        "storage_temperature": 2.0,
        "storage_humidity": 85.0,
        "packaging_type": "Vacuum Sealed",
        "storage_duration": 1
    }, headers=headers)
    inv_id = inv_res.json()["id"]

    # Ingest 3 simulated IoT sensor pings
    readings = [
        {"temperature": 2.2, "humidity": 85.0, "storage_location": "Vault A1", "notes": "Reading 1"},
        {"temperature": 2.5, "humidity": 86.0, "storage_location": "Vault A1", "notes": "Reading 2"},
        {"temperature": 9.4, "humidity": 84.0, "storage_location": "Vault A1", "notes": "Door opened - thermal breach"}
    ]

    res = client.post("/api/storage-conditions/batch-telemetry", json={
        "inventory_id": inv_id,
        "sensor_id": "SENSOR-COLD-99",
        "readings": readings
    }, headers=headers)

    assert res.status_code == 201
    data = res.json()
    assert data["ingested_count"] == 3
    assert data["latest_temperature"] == 9.4
    assert data["latest_humidity"] == 84.0
    assert any("Thermal breach" in a for a in data["alerts_triggered"])

    # Verify inventory was synchronized with latest sensor reading
    inv_check = client.get(f"/api/inventory/{inv_id}", headers=headers)
    assert inv_check.status_code == 200
    assert inv_check.json()["storage_temperature"] == 9.4

def test_batch_telemetry_safe_limits_and_validation(client, retail_token):
    headers = {"Authorization": f"Bearer {retail_token}"}

    # 1. Invalid temperature (e.g. 75°C > 60°C)
    res_invalid_temp = client.post("/api/storage-conditions/batch-telemetry", json={
        "inventory_id": 1,
        "sensor_id": "SENSOR-COLD-01",
        "readings": [{"temperature": 75.0, "humidity": 80.0}]
    }, headers=headers)
    assert res_invalid_temp.status_code == 422

    # 2. Invalid humidity (e.g. 110% > 100%)
    res_invalid_hum = client.post("/api/storage-conditions/batch-telemetry", json={
        "inventory_id": 1,
        "sensor_id": "SENSOR-COLD-01",
        "readings": [{"temperature": 4.0, "humidity": 110.0}]
    }, headers=headers)
    assert res_invalid_hum.status_code == 422

    # 3. Exceeding max batch limit of 50 readings
    oversized_readings = [{"temperature": 4.0, "humidity": 85.0} for _ in range(51)]
    res_oversized = client.post("/api/storage-conditions/batch-telemetry", json={
        "inventory_id": 1,
        "sensor_id": "SENSOR-COLD-01",
        "readings": oversized_readings
    }, headers=headers)
    assert res_oversized.status_code == 422
