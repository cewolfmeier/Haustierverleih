import pytest


def test_get_animal_types(client, auth):
    response = client.get(
        "api/v0/animaltypes/", headers={"Authorization": "Bearer " + auth.token}
    )
    assert response.status_code == 200
    assert len(response.json) > 1


@pytest.mark.parametrize(
    ("req_id", "resp_key", "status_code"),
    (
        ("1", "animalTypeId", 200),
        ("99", "messages", 404),
    ),
)
def test_get_animal_type_by_id(client, auth, req_id, resp_key, status_code):
    response = client.get(
        "api/v0/animaltypes/" + req_id,
        headers={"Authorization": "Bearer " + auth.admin_token},
    )
    assert response.status_code == status_code
    assert resp_key in response.json


@pytest.mark.parametrize(
    ("req_data", "resp_key", "status_code"),
    (
        ({"animalType": "cat"}, "animalTypeId", 201),
        (
            {"animalType": "cat", "animalTypeId": 99},  # animalTypeId is not allowed
            "messages",
            400,
        ),
        ({"animalType": "dog"}, "messages", 400),  # anmial_type has to be unique
        ({"animal_type": "cat"}, "messages", 400),  # key has to be in camelCase
        ({"animalType": 1}, "messages", 400),  # value has to be a string
    ),
)
def test_post(client, auth, req_data, resp_key, status_code):
    response = client.post(
        "api/v0/animaltypes/",
        json=req_data,
        headers={"Authorization": "Bearer " + auth.admin_token},
    )
    assert response.status_code == status_code
    assert resp_key in response.json


@pytest.mark.parametrize(
    ("req_data", "resp_key", "status_code"),
    (
        ({"animalType": "cat"}, "animalType", 200),
        (
            {"animalType": "cat", "animalTypeId": 99},  # animalTypeId is not allowed
            "messages",
            400,
        ),
        ({"animalType": "dog"}, "messages", 400),  # anmial_type has to be unique
        ({"animal_type": "cat"}, "messages", 400),  # key has to be in camelCase
        ({"animalType": 1}, "messages", 400),  # value has to be a string
    ),
)
def test_put(client, auth, req_data, resp_key, status_code):
    """Try to change the animal type"""
    response = client.put(
        "api/v0/animaltypes/2",
        json=req_data,
        headers={"Authorization": "Bearer " + auth.admin_token},
    )
    assert response.status_code == status_code
    assert resp_key in response.json


@pytest.mark.parametrize(
    ("req_id", "resp_key", "status_code"),
    (
        ("3", None, 204),
        ("99", "messages", 404),
        ("1", "messages", 409),  # should not delete element when a pet is still tied to it
    ),
)
def test_delete(client, auth, req_id, resp_key, status_code):
    response = client.delete(
        "api/v0/animaltypes/" + req_id,
        headers={"Authorization": "Bearer " + auth.admin_token},
    )
    assert response.status_code == status_code
    if resp_key:
        assert resp_key in response.json
