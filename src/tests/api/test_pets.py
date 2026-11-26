import pytest


@pytest.mark.parametrize(
    ("query_param", "resp_key"),
    (
        ("", "borrower"),  # Thou shalt see all pets
        ("?borrowed", "borrower"),  # Thou shalt see pets borrowed by thyself
        ("?owned", "borrower"),  # Thou shalt see pets owned by thyself
    ),
)
def test_get_collection(client, auth, query_param, resp_key):
    response = client.get(
        "api/v0/pets/" + query_param, headers={"Authorization": "Bearer " + auth.token}
    )
    assert response.status_code == 200, "Happy Path, should return okay"
    assert len(response.json) > 1


@pytest.mark.parametrize(
    ("req_id", "resp_keys", "status_code"),
    (
        ("1", ["animalType", "borrower", "owner"], 200),  # include ForeignKey Objects
        ("99", ["messages"], 404),
    ),
)
def test_get_by_id(client, auth, req_id, resp_keys, status_code):
    response = client.get(
        "api/v0/pets/" + req_id, headers={"Authorization": "Bearer " + auth.token}
    )
    assert response.status_code == status_code
    for key in resp_keys:
        assert key in response.json


@pytest.mark.parametrize(
    ("req_data", "resp_key", "status_code"),
    (
        (
            {"name": "Milo", "description": "A little cat", "animalTypeId": 1},
            "petId",
            201,
        ),
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
        ),  # Thou shalt not use wrong value types
        (
            {
                "name": "Milo",
                "description": "A little cat",
                "animalTypeId": 1,
                "myCustom": "Hello!",
            },
            "messages",
            400,
        ),  # Thou shalt reject unkown keys
    ),
)
def test_post(client, auth, req_data, resp_key, status_code):
    response = client.post(
        "api/v0/pets/", json=req_data, headers={"Authorization": "Bearer " + auth.token}
    )
    assert response.status_code == status_code
    assert resp_key in response.json


@pytest.mark.parametrize(
    ("req_id", "req_data", "resp_key", "status_code"),
    (
        (
            "3",
            {"name": "Milo", "description": "A little cat", "animalTypeId": 1},
            "petId",
            200,
        ),
        (
            "2",
            {"name": "Milo", "description": "A little cat", "animalTypeId": 1},
            "messages",
            403,
        ),  # Thou shalt only edit own pets
        (
            "99",
            {"name": "Milo", "description": "A little cat", "animalTypeId": 1},
            "messages",
            404,
        ),
        (
            "2",
            {"name": "Milo", "description": "A little cat"},
            "messages",
            400,
        ),  # Thou shalt not send incomplete request bodies
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
        ),  # Thou shalt not include petId
        (
            "2",
            {"name": "Milo", "description": "A little cat", "animal_type_id": 1},
            "messages",
            400,
        ),  # Thou shalt always use camelCase
        (
            "2",
            {"name": 123, "description": "A little cat", "animalTypeId": 1},
            "messages",
            400,
        ),  # Thou shalt not use wrong value types
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
        ),  # Thou shalt reject unkown keys
        ("2", {}, "messages", 400),  # Thou shalt not send an empty body
    ),
)
def test_put(client, auth, req_id, req_data, resp_key, status_code):
    response = client.put(
        "api/v0/pets/" + req_id,
        json=req_data,
        headers={"Authorization": "Bearer " + auth.token},
    )
    assert response.status_code == status_code
    assert resp_key in response.json


@pytest.mark.parametrize(
    ("req_id", "resp_key", "status_code"),
    (
        ("3", None, 204),
        ("1", "messages", 403),  # Thou shalt only delete own pet
        ("99", "messages", 404),
    ),
)
def test_delete(client, auth, req_id, resp_key, status_code):
    response = client.delete(
        "api/v0/pets/" + req_id, headers={"Authorization": "Bearer " + auth.token}
    )
    assert response.status_code == status_code
    if resp_key:
        assert resp_key in response.json


@pytest.mark.parametrize(
    ("req_id", "resp_key", "status_code"),
    (
        ("2", "petId", 200),
        ("3", "messages", 403),  # Thou shalt not borrow own pets
        (
            "1",
            "messages",
            400,
        ),  # Thou shalt not borrow borrowed pets
        ("99", "messages", 404),
    ),
)
def test_borrow(client, auth, req_id, resp_key, status_code):
    response = client.patch(
        f"api/v0/pets/{req_id}/borrow",
        headers={"Authorization": "Bearer " + auth.token},
    )
    assert response.status_code == status_code
    assert resp_key in response.json


@pytest.mark.parametrize(
    ("req_id", "resp_key", "status_code"),
    (
        ("1", "petId", 200),
        ("4", "messages", 403),  # Thou shalt not return others borrowed pets
        ("3", "messages", 403),  # Thou shalt not return own or available pets
        ("99", "messages", 404),
    ),
)
def test_return(client, auth, req_id, resp_key, status_code):
    response = client.patch(
        f"api/v0/pets/{req_id}/return",
        headers={"Authorization": "Bearer " + auth.token},
    )
    assert response.status_code == status_code
    assert resp_key in response.json


"""
@pytest.mark.parametrize(
    ("req_id", "req_data", "resp_key", "status_code"),
    (
        ("2", {}, "petId", 200),
        ("2", {"borrowerId": 2}, "messages", 400),  # no properties allowed
        ("99", {}, "messages", 404),
    ),
)
def test_update_picture(client, auth, req_id, req_data, resp_key, status_code):
    response = client.patch(
        f"api/v0/pets/{req_id}/picture",
        json=req_data,
        headers={"Authorization": "Bearer " + auth.token},
    )
    assert response.status_code == status_code
    assert resp_key in response.json


@pytest.mark.parametrize(
    ("req_id", "req_data", "resp_key", "status_code"),
    (
        ("2", {}, "petId", 200),  # happy path
        ("2", {"borrowerId": 2}, "messages", 400),  # no properties allowed
        ("99", {}, "messages", 404),  # wrong id
    ),
)
def test_get_picture(client, auth, req_id, req_data, resp_key, status_code):
    response = client.get(
        f"api/v0/pets/{req_id}/picture",
        json=req_data,
        headers={"Authorization": "Bearer " + auth.token},
    )
    assert response.status_code == status_code
    assert resp_key in response.json


@pytest.mark.parametrize(
    ("req_id", "req_data", "resp_key", "status_code"),
    (
        ("2", {}, "petId", 200),  # happy path
        ("2", {"borrowerId": 2}, "messages", 400),  # no properties allowed
        ("99", {}, "messages", 404),  # wrong id
    ),
)
def test_delete_picture(client, auth, req_id, req_data, resp_key, status_code):
    response = client.get(
        f"api/v0/pets/{req_id}/picture",
        json=req_data,
        headers={"Authorization": "Bearer " + auth.token},
    )
    assert response.status_code == status_code
    assert resp_key in response.json
"""
