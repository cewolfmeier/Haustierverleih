import base64

import pytest


@pytest.mark.parametrize(
    ("req_data", "resp_key", "status_code"),
    (
        (
            {"username": "herbert", "password": "MySecretPassword1!"},
            "userId",
            201,
        ),  # happy path
        (
            {"username": "herbert", "password": "MySecretPassword1!", "userId": 99},
            "messages",
            400,
        ),  # petId is not allowed
        (
            {"username": "herbert", "password": "MySecretPassword1!", "role_id": 1},
            "messages",
            400,
        ),  # key has to be in camelCase
        (
            {"username": "herbert", "password": "MySecretPassword1!", "roleId": 1},
            "messages",
            400,
        ),  # Role should not be set in request body on register
        (
            {"username": 42, "password": "MySecretPassword1!"},
            "messages",
            400,
        ),  # wrong value type
        (
            {
                "username": "herbert",
                "password": "MySecretPassword1!",
                "myCustom": "Hello!",
            },
            "messages",
            400,
        ),  # reject unkown keys
        ({}, "messages", 400),  # reject empty bodies
    ),
)
def test_register(client, req_data, resp_key, status_code):
    response = client.post("api/v0/register", json=req_data)
    assert response.status_code == status_code
    # assert resp_key in response.json


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
        ),  # happy path
        (
            {
                "Authorization": "Basic "
                + base64.b64encode(b"toast:test").decode("utf-8")
            },
            "msg",
            401,
        ),  # wrong username
        (
            {
                "Authorization": "Basic "
                + base64.b64encode(b"test:toast").decode("utf-8")
            },
            "msg",
            401,
        ),  # wrong password
        (
            {"Authorization": "Basic " + base64.b64encode(b":").decode("utf-8")},
            "msg",
            401,
        ),  # missing credentials
        (
            {"Authorization": ""},
            "msg",
            401,
        ),  # missing value
        (
            {},
            "msg",
            401,
        ),  # empty header
        ({}, "msg", 401),  # reject empty bodies
    ),
)
def test_login(client, headers, resp_key, status_code):
    response = client.post("api/v0/login", headers=headers)
    assert response.status_code == status_code
    # assert resp_key in response.json


@pytest.mark.parametrize(
    ("resource",),
    (
        ("/animaltypes",),
        ("/animaltypes/1",),
        ("/pets/1",),
        ("/pets",),
        ("/users",),
        ("/users/1",),
    ),
)
def test_protected_get_routes(client, auth, resource):
    response = client.get("api/v0" + resource)
    assert response.status_code == 401
    response = client.get(
        "api/v0" + resource, headers={"Authorization": "Bearer " + auth.token}
    )
    assert response.status_code == 200
