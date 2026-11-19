import pytest


def test_get_collection(client):
    response = client.get("api/v0/pets")
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
    response = client.get("api/v0/pets/" + id)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("req_data", "resp_key", "status_code"),
    (
        (
            {"name": "Milo", "description": "A little cat", "animalTypeId": 1},
            "petId",
            201,
        ),  # happy path
        (
            {
                "name": "Milo",
                "description": "A little cat",
                "animalTypeId": 1,
                "petId": 99,
            },
            "messages",
            400,
        ),  # petId is not allowed
        (
            {"name": "Milo", "description": "A little cat", "animal_type_id": 1},
            "messages",
            400,
        ),  # key has to be in camelCase
        (
            {"name": 123, "description": "A little cat", "animalTypeId": 1},
            "messages",
            400,
        ),  # wrong value type
        (
            {
                "name": "Milo",
                "description": "A little cat",
                "animalTypeId": 1,
                "myCustom": "Hello!",
            },
            "messages",
            400,
        ),  # reject unkown keys
        ({}, "messages", 400),  # reject empty bodies
    ),
)
def test_post(client, req_data, resp_key, status_code):
    response = client.post("api/v0/pets", json=req_data)
    assert response.status_code == status_code
    # assert resp_key in response.json


@pytest.mark.parametrize(
    ("id", "req_data", "resp_key", "status_code"),
    (
        (
            "2",
            {"name": "Milo", "description": "A little cat", "animalTypeId": 1},
            "petId",
            200,
        ),  # happy path
        (
            "99",
            {"name": "Milo", "description": "A little cat", "animalTypeId": 1},
            "messages",
            404,
        ),  # wrong id
        (
            "2",
            {"name": "Milo", "description": "A little cat"},
            "messages",
            400,
        ),  # missing key:value
        (
            "2",
            {
                "name": "Milo",
                "description": "A little cat",
                "animalTypeId": 1,
                "petId": 99,
            },
            "messages",
            400,
        ),  # petId is not allowed
        (
            "2",
            {"name": "Milo", "description": "A little cat", "animal_type_id": 1},
            "messages",
            400,
        ),  # key has to be in camelCase
        (
            "2",
            {"name": 123, "description": "A little cat", "animalTypeId": 1},
            "messages",
            400,
        ),  # wrong value type
        (
            "2",
            {
                "name": "Milo",
                "description": "A little cat",
                "animalTypeId": 1,
                "myCustom": "Hello!",
            },
            "messages",
            400,
        ),  # reject unkown keys
        ("2", {}, "messages", 400),  # reject empty bodies
    ),
)
def test_put(client, id, req_data, resp_key, status_code):
    response = client.put("api/v0/pets/" + id, json=req_data)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("id", "req_data", "resp_key", "status_code"),
    (
        ("2", {"name": "Milo"}, "petId", 200),  # happy path
        ("99", {"name": "Milo"}, "messages", 404),  # wrong id
        ("2", {"petId": 99}, "messages", 400),  # petId is not allowed
        ("2", {"animal_type_id": 1}, "messages", 400),  # key has to be in camelCase
        ("2", {"name": 123}, "messages", 400),  # wrong value type
        ("2", {"myCustom": "Hello!"}, "messages", 400),  # reject unkown keys
    ),
)
def test_patch(client, id, req_data, resp_key, status_code):
    response = client.patch("api/v0/pets/" + id, json=req_data)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("id", "status_code"),
    (
        ("1", 204),  # happy path
        ("99", 404),  # throw not found error
    ),
)
def test_delete(client, id, status_code):
    response = client.delete("api/v0/pets/" + id)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("id", "req_data", "resp_key", "status_code"),
    (
        ("2", {}, "petId", 200),  # happy path
        ("2", {"borrowerId": 2}, "messages", 400),  # no properties allowed
        ("99", {}, "messages", 404),  # wrong id
    ),
)
def test_borrow(client, id, req_data, resp_key, status_code):
    response = client.patch(f"api/v0/pets/{id}/borrow", json=req_data)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("id", "req_data", "resp_key", "status_code"),
    (
        ("2", {}, "petId", 200),  # happy path
        ("2", {"borrowerId": 2}, "messages", 400),  # no properties allowed
        ("99", {}, "messages", 404),  # wrong id
    ),
)
def test_return(client, id, req_data, resp_key, status_code):
    response = client.patch(f"api/v0/pets/{id}/return", json=req_data)
    assert response.status_code == status_code
