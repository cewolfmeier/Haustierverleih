import base64

import pytest

headers = {"Authorization": "Basic " + base64.b64encode(b"test:test").decode("utf-8")}
invalid_user_header = {
    "Authorization": "Basic " + base64.b64encode(b"toast:test").decode("utf-8")
}
invalid_password_header = {
    "Authorization": "Basic " + base64.b64encode(b"test:toast").decode("utf-8")
}


# ------ Login Route ------
def test_refuse_login_without_auth_header(client):
    response = client.post("api/v0/login")
    assert response.status_code == 401


def test_refuse_login_with_invalid_credentials(client):
    response = client.post("api/v0/login", headers=invalid_user_header)
    assert response.status_code == 401
    response = client.post("api/v0/login", headers=invalid_password_header)
    assert response.status_code == 401


def test_login_happy_path(client):
    response = client.post("api/v0/login", headers=headers)
    assert response.status_code == 200
    assert "Set-Cookie" in response.headers
    assert "jwt" in response.headers["Set-Cookie"]
    assert response.json == {"userId": 1, "username": "test", "isAdmin": False}
    response = client.get("api/v0/animaltypes")
    assert response.status_code == 200


# ------ Token Auth ------
@pytest.mark.parametrize(
    ("route",),
    (
        ("/animaltypes",),
        ("/me",),
        ("/me/pets",),
        ("/me/pets/1",),
        ("/pets",),
        ("/pets/1",),
        ("/users",),
    ),
)
def test_get_requests_without_token_respond_with_401(client, route: str):
    response = client.get(f"api/v0{route}")
    assert response.status_code == 401
