import pytest


def test_get_animal_types(client):
    response = client.get("api/v0/animaltypes")
    assert response.status_code == 200, "Happy Path, should return okay"
    assert len(response.json) > 1


def test_get_animal_type_by_id(client):
    response = client.get("api/v0/animaltypes/1")
    assert response.status_code == 200, "Happy Path, should return okay"
    assert "animalType" in response.json, "JSON body is not empty, key is in camelCase"


def test_get_non_prestent_animal_type(client):
    response = client.get("api/v0/animaltypes/99")
    assert response.status_code == 404, "Not present, throw 404 Error"


@pytest.mark.parametrize(
    ("req_data", "resp_key", "status_code"),
    (
        ({"animalType": "cat"}, "animalTypeId", 201),  # happy path
        (
            {"animalType": "cat", "animalTypeId": 99},
            "messages",
            400,
        ),  # animalTypeId is not allowed in post requests
        ({"animalType": "dog"}, "messages", 400),  # anmial_type has to be unique
        ({"animal_type": "cat"}, "messages", 400),  # key has to be in camelCase
        ({"animalType": 1}, "messages", 400),  # value has to be a string
        (
            {"myType": "lizard", "animalType": "lizard"},
            "messages",
            400,
        ),  # reject unkown keys
        ({}, "messages", 400),  # reject empty bodies
    ),
)
def test_post(client, req_data, resp_key, status_code):
    response = client.post("api/v0/animaltypes", json=req_data)
    assert response.status_code == status_code
    # assert resp_key in response.json


@pytest.mark.parametrize(
    ("req_data", "resp_key", "status_code"),
    (
        ({"animalType": "cat"}, "animalType", 200),  # happy path
        (
            {"animalType": "cat", "animalTypeId": 99},
            "messages",
            400,
        ),  # animalTypeId is not allowed in put requests
        ({"animalType": "dog"}, "messages", 400),  # anmial_type has to be unique
        ({"animal_type": "cat"}, "messages", 400),  # key has to be in camelCase
        ({"animalType": 1}, "messages", 400),  # value has to be a string
        (
            {"myType": "lizard", "animalType": "lizard"},
            "messages",
            400,
        ),  # reject unkown keys
        ({}, "messages", 400),  # reject empty bodies
    ),
)
def test_put(client, req_data, resp_key, status_code):
    """Try to change the animal type 'fish'"""
    response = client.put("api/v0/animaltypes/2", json=req_data)
    assert response.status_code == status_code


# Same like put
@pytest.mark.parametrize(
    ("req_data", "resp_key", "status_code"),
    (
        ({"animalType": "cat"}, "animalType", 200),  # happy path
        (
            {"animalType": "cat", "animalTypeId": 99},
            "messages",
            400,
        ),  # animalTypeId is not allowed in put requests
        ({"animalType": "dog"}, "messages", 400),  # anmial_type has to be unique
        ({"animal_type": "cat"}, "messages", 400),  # key has to be in camelCase
        ({"animalType": 1}, "messages", 400),  # value has to be a string
        (
            {"myType": "lizard", "animalType": "lizard"},
            "messages",
            400,
        ),  # reject unkown keys
        ({}, "messages", 400),  # reject empty bodies
    ),
)
def test_patch(client, req_data, resp_key, status_code):
    """Try to change the animal type 'fish'"""
    response = client.patch("api/v0/animaltypes/2", json=req_data)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("id", "status_code"),
    (
        ("1", 204),  # happy path
        ("99", 404),  # throw not found error
    ),
)
def test_delete(client, id, status_code):
    response = client.delete("api/v0/animaltypes/" + id)
    assert response.status_code == status_code
