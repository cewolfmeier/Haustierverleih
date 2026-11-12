def test_users(client):
    response = client.get("api/v0/users")
    assert response.status_code == 200, "Happy Path, should return okay"
    assert response.json == []


def test_register_new_user(client):
    response = client.post(
        "api/v0/users",
        json={
            "username": "herta",
            "password": "herta",
        },
    )
    assert response.status_code == 201, "Happy Path, should return created"


def test_register_with_taken_username(client):
    client.post(
        "api/v0/users",
        json={"username": "herbert", "password": "herbert"},
    )
    response = client.post(
        "api/v0/users",
        json={"username": "herbert", "password": "herbert"},
    )
    assert response.status_code == 400, "New user creation should return bad request"
