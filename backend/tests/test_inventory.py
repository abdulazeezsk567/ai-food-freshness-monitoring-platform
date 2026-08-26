from datetime import date, timedelta

def test_create_and_get_inventory(client, retail_token):
    headers = {"Authorization": f"Bearer {retail_token}"}
    food_res = client.post("/api/food-items", json={
        "name": "Test Cheddar Cheese",
        "category": "Dairy Products",
        "description": "Aged sharp cheddar cheese block"
    }, headers=headers)
    food_id = food_res.json()["id"]

    today = date.today()
    exp_date = str(today + timedelta(days=15))

    inv_res = client.post("/api/inventory", json={
        "food_item_id": food_id,
        "batch_number": "BATCH-CHS-999",
        "quantity": 10.0,
        "unit": "kg",
        "purchase_date": str(today),
        "expiry_date": exp_date,
        "storage_temperature": 3.0,
        "storage_humidity": 80.0,
        "packaging_type": "Wax Sealed",
        "storage_duration": 15
    }, headers=headers)
    assert inv_res.status_code == 201
    data = inv_res.json()
    assert data["batch_number"] == "BATCH-CHS-999"
    assert data["status"] == "Fresh"
    assert data["days_to_expiry"] == 15

def test_dashboard_stats(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    res = client.get("/api/stats/dashboard", headers=headers)
    assert res.status_code == 200
    stats = res.json()
    assert "total_food_items" in stats
    assert "active_batches" in stats
    assert "expiring_soon" in stats
    assert "expired_items" in stats
