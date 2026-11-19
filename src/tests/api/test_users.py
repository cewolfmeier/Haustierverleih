def test_get_users(client):
    response = client.get("api/v0/users")
    assert response.status_code == 200, "Happy Path, should return okay"
    assert response.json == []
