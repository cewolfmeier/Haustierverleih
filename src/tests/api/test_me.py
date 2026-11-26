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
            {"passwordOld": "test", "passwordNew": "MySecretPassword1!"},
            None,
            200,
        ),
        (
            {"passwordOld": "toast", "passwordNew": "MySecretPassword1!"},
            "msg",
            400,  # Thou shalt reject wrong old passwords
        ),
        (
            {"passwordNew": "MySecretPassword1!"},
            "msg",
            400,  # Thou shalt reject missing key:value pairs
        ),
        ("2", {}, "msg", 400),  # reject empty bodies
    ),
)
def test_update_password(client, auth, req_data, resp_key, status_code):
    response = client.put(
        "api/v0/me/",
        json=req_data,
        headers={"Authorization": "Bearer " + auth.admin_token},
    )
    assert response.status_code == status_code
    assert resp_key in response.json


@pytest.mark.parametrize(
    ("req_id", "req_data", "resp_key", "status_code"),
    (
        (
            {"username": "herta"},
            None,
            200,
        ),
        (
            {"username": "test"},
            None,
            200,
        ),  # Thou shalt accept users current username
        (
            {"username": "admin"},
            "msg",
            400,
        ),  # Thou shalt reject taken usernames
        (
            {"username": ""},
            "msg",
            400,
        ),  # Thou shalt reject empty strings
        ("2", {}, "msg", 400),  # reject empty bodies
    ),
)
def test_update_username(client, auth, req_id, req_data, resp_key, status_code):
    response = client.put(
        "api/v0/me/" + req_id,
        json=req_data,
        headers={"Authorization": "Bearer " + auth.admin_token},
    )
    assert response.status_code == status_code
    assert resp_key in response.json


def test_delete_me(client, auth):
    response = client.delete(
        "api/v0/me/", headers={"Authorization": "Bearer " + auth.token}
    )
    assert response.status_code == 204
    assert response.headers
