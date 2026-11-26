import pytest


def test_get_collection(client, auth):
    response = client.get(
        "api/v0/users/", headers={"Authorization": "Bearer " + auth.admin_token}
    )
    assert response.status_code == 200, "Happy Path, should return okay"
    assert len(response.json) > 1


@pytest.mark.parametrize(
    ("req_id", "resp_key", "status_code"),
    (
        ("1", "role", 200),  # include Roles Object
        ("99", "messages", 404),
    ),
)
def test_get_by_id(client, auth, req_id, resp_key, status_code):
    response = client.get(
        "api/v0/users/" + req_id,
        headers={"Authorization": "Bearer " + auth.admin_token},
    )
    assert response.status_code == status_code
    assert resp_key in response.json


@pytest.mark.parametrize(
    ("req_id", "req_data", "resp_key", "status_code"),
    (
        ("2", {"roleId": 1}, "userId", 200),
        ("99", {"roleId": 1}, "messages", 404),
        (
            "2",
            {"roleId": 1, "userId": 99},
            "messages",
            400,
        ),  # userId is not allowed
        ("2", {"role_id": 1}, "messages", 400),  # key has to be in camelCase
        ("2", {"roleId": "A"}, "messages", 400),  # wrong value type
        ("2", {"roleId": 99}, "messages", 404),  # role not available
    ),
)
def test_patch(client, auth, req_id, req_data, resp_key, status_code):
    response = client.patch(
        f"api/v0/users/{req_id}/roles",
        json=req_data,
        headers={"Authorization": "Bearer " + auth.admin_token},
    )
    assert response.status_code == status_code
    assert resp_key in response.json


@pytest.mark.parametrize(
    ("req_id", "resp_key", "status_code"),
    (
        ("1", None, 204),
        ("99", "messages", 404),
    ),
)
def test_delete(client, auth, req_id, resp_key, status_code):
    response = client.delete(
        "api/v0/users/" + req_id,
        headers={"Authorization": "Bearer " + auth.admin_token},
    )
    assert response.status_code == status_code
    if resp_key:
        assert resp_key in response.json
