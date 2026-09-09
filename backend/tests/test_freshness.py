import os
import io
import pytest
from PIL import Image

def create_dummy_image_bytes(format="JPEG", color=(0, 200, 0), size=(200, 200)) -> bytes:
    img = Image.new("RGB", size, color=color)
    buf = io.BytesIO()
    img.save(buf, format=format)
    return buf.getvalue()

def test_upload_image_success(client, retail_token):
    img_bytes = create_dummy_image_bytes(format="JPEG")
    files = {"file": ("test_apple.jpg", img_bytes, "image/jpeg")}
    headers = {"Authorization": f"Bearer {retail_token}"}
    
    response = client.post("/api/freshness/upload", files=files, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "image_path" in data
    assert data["image_path"].startswith("/uploads/freshness/")

def test_upload_image_invalid_type(client, retail_token):
    files = {"file": ("test_script.sh", b"echo hello", "text/x-sh")}
    headers = {"Authorization": f"Bearer {retail_token}"}
    
    response = client.post("/api/freshness/upload", files=files, headers=headers)
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]

def test_analyze_freshness_success(client, retail_token):
    img_bytes = create_dummy_image_bytes(format="PNG", color=(50, 180, 50))
    files = {"file": ("fresh_spinach.png", img_bytes, "image/png")}
    data = {"food_category": "Vegetables"}
    headers = {"Authorization": f"Bearer {retail_token}"}

    response = client.post("/api/freshness/analyze", files=files, data=data, headers=headers)
    assert response.status_code == 201
    res = response.json()
    assert res["food_category"] == "Vegetables"
    assert res["predicted_category"] in ["Fresh", "Good", "Acceptable", "Near Spoilage", "Spoiled"]
    assert 0 <= res["freshness_score"] <= 100
    assert 0.0 <= res["spoilage_probability"] <= 1.0
    assert 0.0 <= res["confidence"] <= 1.0
    assert "color_analysis" in res
    assert "texture_analysis" in res
    assert "spoilage_indicators" in res

def test_list_and_get_analysis_results(client, retail_token):
    headers = {"Authorization": f"Bearer {retail_token}"}
    
    list_res = client.get("/api/freshness/results", headers=headers)
    assert list_res.status_code == 200
    results = list_res.json()
    assert len(results) > 0

    item_id = results[0]["id"]
    get_res = client.get(f"/api/freshness/results/{item_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["id"] == item_id

def test_inventory_freshness_history(client, retail_token):
    headers = {"Authorization": f"Bearer {retail_token}"}
    
    # 1. Create a food item and batch
    food_res = client.post("/api/food-items", json={
        "name": "Test Avocado Batch Item",
        "category": "Fruits",
        "description": "Avocado batch for freshness history testing"
    }, headers=headers)
    food_id = food_res.json()["id"]

    inv_res = client.post("/api/inventory", json={
        "food_item_id": food_id,
        "batch_number": "BATCH-AVO-TEST",
        "quantity": 5.0,
        "unit": "kg",
        "purchase_date": "2026-09-01",
        "expiry_date": "2026-09-15",
        "storage_temperature": 4.0,
        "storage_humidity": 85.0,
        "packaging_type": "Plastic Tray",
        "storage_duration": 14
    }, headers=headers)
    inv_id = inv_res.json()["id"]

    # 2. Perform image analysis linked to this inventory batch
    img_bytes = create_dummy_image_bytes()
    files = {"file": ("avocado.jpg", img_bytes, "image/jpeg")}
    data = {"food_category": "Fruits", "inventory_id": str(inv_id)}
    
    an_res = client.post("/api/freshness/analyze", files=files, data=data, headers=headers)
    assert an_res.status_code == 201

    # 3. Retrieve history for this inventory batch
    history_res = client.get(f"/api/freshness/inventory/{inv_id}/freshness-history", headers=headers)
    assert history_res.status_code == 200
    history = history_res.json()
    assert len(history) == 1
    assert history[0]["inventory_id"] == inv_id
