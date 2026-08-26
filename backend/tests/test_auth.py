import uuid

def test_register_user(client):
    unique_email = f"user_{uuid.uuid4().hex[:6]}@example.com"
    response = client.post("/api/auth/register", json={
        "name": "Test User",
        "email": unique_email,
        "password": "Password123!",
        "role": "CONSUMER"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == unique_email
    assert data["role"] == "CONSUMER"
    assert "password_hash" not in data

def test_login_user(client):
    response = client.post("/api/auth/login", json={
        "email": "admin@foodfreshness.com",
        "password": "Admin123!"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "admin@foodfreshness.com"

def test_login_invalid_password(client):
    response = client.post("/api/auth/login", json={
        "email": "admin@foodfreshness.com",
        "password": "WrongPassword!"
    })
    assert response.status_code == 401

def test_get_me(client, admin_token):
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin@foodfreshness.com"
    assert data["role"] == "ADMINISTRATOR"
