import base64

import pytest


@pytest.mark.parametrize(
    ("req_data", "resp_key", "status_code"),
    (
        (
            {"username": "herbert", "password": "MySecretPassword1!"},
            "userId",
            201,
        ),
        (
            {"username": "herbert", "password": "MySecretPassword1!", "userId": 99},
            "messages",
            400,
        ),
        (
            {"username": "herbert", "password": "MySecretPassword1!", "role_id": 1},
            "messages",
            400,
        ),
        (
            {"username": "herbert", "password": "MySecretPassword1!", "roleId": 1},
            "messages",
            400,
        ),
        (
            {"username": 42, "password": "MySecretPassword1!"},
            "messages",
            400,
        ),
        (
            {
                "username": "herbert",
                "password": "MySecretPassword1!",
                "myCustom": "Hello!",
            },
            "messages",
            400,
        ),
        ({}, "messages", 400),
    ),
)
def test_register(client, req_data, resp_key, status_code):
    response = client.post("api/v0/register", json=req_data)
    assert response.status_code == status_code
    assert resp_key in response.json


@pytest.mark.parametrize(
    ("headers", "resp_key", "status_code"),
    (
        (
            {
                "Authorization": "Basic "
                + base64.b64encode(b"test:test").decode("utf-8")
            },
            "accessToken",
            200,
        ),
        (
            {
                "Authorization": "Basic "
                + base64.b64encode(b"toast:test").decode("utf-8")
            },
            "messages",
            401,
        ),
        (
            {
                "Authorization": "Basic "
                + base64.b64encode(b"test:toast").decode("utf-8")
            },
            "messages",
            401,
        ),
        (
            {"Authorization": "Basic " + base64.b64encode(b":").decode("utf-8")},
            "messages",
            401,
        ),
        (
            {"Authorization": ""},
            "messages",
            401,
        ),
        (
            {},
            "messages",
            401,
        ),
    ),
)
def test_login(client, headers, resp_key, status_code):
    response = client.post("api/v0/login", headers=headers)
    assert response.status_code == status_code
    assert resp_key in response.json


def test_logout(client, auth):
    response = client.delete(
        "api/v0/logout", headers={"Authorization": "Bearer " + auth.token}
    )
    assert response.status_code == 204
    assert response.headers


def test_token_rotation(client):
    client.post("api/v0/login")  # set refresh cookie
    response = client.put("api/v0/tokens")
    assert response.status_code == 200
    assert "access_token" in response.json
    assert "Set-Cookie" in response.headers


@pytest.mark.parametrize(
    ("path",),
    (
        ("/animaltypes/",),
        ("/animaltypes/1",),
        ("/pets/1",),
        ("/pets/",),
        ("/users/",),
        ("/users/1",),
        ("/me/",),
    ),
)
def test_protected_get_routes(client, path):
    response = client.get("api/v0" + path)
    assert response.status_code == 401


@pytest.mark.parametrize(
    ("path",),
    (
        ("/animaltypes/",),
        ("/pets/",),
    ),
)
def test_protected_post_routes(client, path):
    response = client.post("api/v0" + path)
    assert response.status_code == 401


@pytest.mark.parametrize(
    ("path",),
    (
        ("/animaltypes/1",),
        ("/pets/1",),
        ("/tokens",),
    ),
)
def test_protected_put_routes(client, path):
    response = client.put("api/v0" + path)
    assert response.status_code == 401


@pytest.mark.parametrize(
    ("path",),
    (
        ("/pets/1/borrow",),
        ("/pets/1/return",),
        ("/users/1/roles",),
        ("/me/password",),
        ("/me/username",),
    ),
)
def test_protected_patch_routes(client, path):
    response = client.patch("api/v0" + path)
    assert response.status_code == 401


@pytest.mark.parametrize(
    ("path",),
    (
        ("/animaltypes/1",),
        ("/pets/1",),
        ("/users/1",),
        ("/me/",),
        ("/logout",),
    ),
)
def test_protected_delete_routes(client, path):
    response = client.delete("api/v0" + path)
    assert response.status_code == 401


@pytest.mark.parametrize(
    ("path",),
    (
        ("/animaltypes/1",),
        ("/users/",),
        ("/users/1",),
    ),
)
def test_private_get_routes(client, auth, path):
    response = client.get(
        "api/v0" + path, headers={"Authorization": "Bearer " + auth.token}
    )
    assert response.status_code == 403


@pytest.mark.parametrize(
    ("path",),
    (("/animaltypes/",),),
)
def test_private_post_routes(client, auth, path):
    response = client.post(
        "api/v0" + path, headers={"Authorization": "Bearer " + auth.token}
    )
    assert response.status_code == 403


@pytest.mark.parametrize(
    ("path",),
    (("/animaltypes/2",),),
)
def test_private_put_routes(client, auth, path):
    response = client.put(
        "api/v0" + path, headers={"Authorization": "Bearer " + auth.token}
    )
    assert response.status_code == 403


@pytest.mark.parametrize(
    ("path",),
    (("/users/1/roles",),),
)
def test_private_patch_routes(client, auth, path):
    response = client.patch(
        "api/v0" + path, headers={"Authorization": "Bearer " + auth.token}
    )
    assert response.status_code == 403


@pytest.mark.parametrize(
    ("path"),
    (
        ("/animaltypes/3"),
        ("/users/2"),
    ),
)
def test_private_delete_routes(client, auth, path):
    response = client.delete(
        "api/v0" + path, headers={"Authorization": "Bearer " + auth.token}
    )
    assert response.status_code == 403
