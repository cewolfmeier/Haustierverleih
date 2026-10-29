
BASE_URL = "api/v0"

def test_animal_types(client):
    response = client.get("/".join([BASE_URL,"animaltypes"]))
    assert response.status_code == 200, "Happy Path, should return okay"
    assert response.json == []

def test_create_new_animal_type(client):
    response = client.post(
        "/".join([BASE_URL,"animaltypes"]),
        json = {"animalType": "dog"},
    )
    assert response.status_code == 201, "Happy Path, should return created"
    assert response.json == {"animalTypeId": 1, "animalType": "dog"}, "Should return the new animal type with id"

def test_create_existing_animal_type(client):
    client.post(
        "/".join([BASE_URL,"animaltypes"]),
        json = {"animalType": "dog"},
    )
    response = client.post(
            "/".join([BASE_URL,"animaltypes"]),
            json = {"animalType": "dog"},
        )
    assert response.status_code == 400, "Should Return bad request"
    