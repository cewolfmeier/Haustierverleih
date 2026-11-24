import pytest


def test_get_collection(client):
    response = client.get("api/v0/users")
    assert response.status_code == 200, "Happy Path, should return okay"
    assert len(response.json) > 1


@pytest.mark.parametrize(
    ("id", "status_code"),
    (
        ("1", 200),  # happy path
        ("99", 404),  # throw not found error
    ),
)
def test_get_by_id(client, id, status_code):
    response = client.get("api/v0/users/" + id)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("id", "req_data", "resp_key", "status_code"),
    (
        (
            "2",
            {"username": "herbert", "password": "MySecretPassword1!"},
            "userId",
            200,
        ),  # happy path
        (
            "99",
            {"username": "herbert", "password": "MySecretPassword1!"},
            "messages",
            404,
        ),  # wrong id
        ("2", {"password": "MySecretPassword1!"}, "messages", 400),  # missing key:value
        (
            "2",
            {"username": "herbert", "password": "MySecretPassword1!", "userId": 99},
            "messages",
            400,
        ),  # userId is not allowed
        (
            "2",
            {"username": "herbert", "password": "MySecretPassword1!", "role_id": 1},
            "messages",
            400,
        ),  # key has to be in camelCase
        (
            "2",
            {"username": 42, "password": "MySecretPassword1!"},
            "messages",
            400,
        ),  # wrong value type
        (
            "2",
            {
                "username": "herbert",
                "password": "MySecretPassword1!",
                "myCustom": "Hello!",
            },
            "messages",
            400,
        ),  # reject unkown keys
        ("2", {}, "messages", 400),  # reject empty bodies
    ),
)
def test_put(client, id, req_data, resp_key, status_code):
    response = client.put("api/v0/users/" + id, json=req_data)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("id", "req_data", "resp_key", "status_code"),
    (
        ("2", {"username": "herbert"}, "userId", 200),  # happy path
        ("99", {"username": "herbert"}, "messages", 404),  # wrong id
        (
            "2",
            {"username": "herbert", "userId": 99},
            "messages",
            400,
        ),  # userId is not allowed
        ("2", {"role_id": 1}, "messages", 400),  # key has to be in camelCase
        ("2", {"username": 42}, "messages", 400),  # wrong value type
        ("2", {"myCustom": "Hello!"}, "messages", 400),  # reject unkown keys
    ),
)
def test_patch(client, id, req_data, resp_key, status_code):
    response = client.patch("api/v0/users/" + id, json=req_data)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("id", "status_code"),
    (
        ("1", 204),  # happy path
        ("99", 404),  # throw not found error
    ),
)
def test_delete(client, id, status_code):
    response = client.delete("api/v0/users/" + id)
    assert response.status_code == status_code
