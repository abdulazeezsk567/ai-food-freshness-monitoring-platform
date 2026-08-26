def test_create_and_list_food_items(client, retail_token):
    headers = {"Authorization": f"Bearer {retail_token}"}
    create_res = client.post("/api/food-items", json={
        "name": "Fresh Strawberries",
        "category": "Fruits",
        "description": "Sweet organic farm-fresh strawberries"
    }, headers=headers)
    assert create_res.status_code == 201
    item = create_res.json()
    assert item["name"] == "Fresh Strawberries"
    assert item["category"] == "Fruits"

    list_res = client.get("/api/food-items", headers=headers)
    assert list_res.status_code == 200
    items = list_res.json()
    assert len(items) > 0

def test_update_food_item(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    create_res = client.post("/api/food-items", json={
        "name": "Green Apples",
        "category": "Fruits",
        "description": "Sour granny smith apples"
    }, headers=headers)
    item_id = create_res.json()["id"]

    update_res = client.put(f"/api/food-items/{item_id}", json={
        "name": "Granny Smith Apples",
        "description": "Updated premium sour granny smith apples"
    }, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["name"] == "Granny Smith Apples"
