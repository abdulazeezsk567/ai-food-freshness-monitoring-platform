def test_list_users_as_admin(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    res = client.get("/api/users", headers=headers)
    assert res.status_code == 200
    users = res.json()
    assert len(users) >= 4

def test_list_users_forbidden_for_consumer(client, consumer_token):
    headers = {"Authorization": f"Bearer {consumer_token}"}
    res = client.get("/api/users", headers=headers)
    assert res.status_code == 403
