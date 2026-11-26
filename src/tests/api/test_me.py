import pytest


def test_get_me(client, auth):
    response = client.get(
        "api/v0/me/", headers={"Authorization": "Bearer " + auth.token}
    )
    assert response.status_code == 200


@pytest.mark.parametrize(
    ("req_data", "resp_key", "status_code"),
    (
        (
            {"passwordOld": "test", "password": "MySecretPassword1!"},
            None,
            200,
        ),
        (
            {"passwordOld": "toast", "password": "MySecretPassword1!"},
            "messages",
            400,  # Thou shalt reject wrong old passwords
        ),
        (
            {"password": "MySecretPassword1!"},
            "messages",
            400,  # Thou shalt reject missing key:value pairs
        ),
        ({}, "messages", 400),  # reject empty bodies
    ),
)
def test_update_password(client, auth, req_data, resp_key, status_code):
    response = client.patch(
        "api/v0/me/password",
        json=req_data,
        headers={"Authorization": "Bearer " + auth.token},
    )
    assert response.status_code == status_code
    if resp_key:
        assert resp_key in response.json


@pytest.mark.parametrize(
    ("req_data", "resp_key", "status_code"),
    (
        (
            {"username": "herta"},
            "userId",
            200,
        ),
        (
            {"username": "test"},
            "userId",
            200,
        ),  # Thou shalt accept users current username
        (
            {"username": "admin"},
            "messages",
            400,
        ),  # Thou shalt reject taken usernames
        (
            {"username": ""},
            "messages",
            400,
        ),  # Thou shalt reject empty strings
        ({}, "messages", 400),  # reject empty bodies
    ),
)
def test_update_username(client, auth, req_data, resp_key, status_code):
    response = client.patch(
        "api/v0/me/username",
        json=req_data,
        headers={"Authorization": "Bearer " + auth.token},
    )
    assert response.status_code == status_code
    assert resp_key in response.json


def test_delete_me(client, auth):
    response = client.delete(
        "api/v0/me/", headers={"Authorization": "Bearer " + auth.token}
    )
    assert response.status_code == 204
