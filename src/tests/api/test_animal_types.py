import pytest

def test_get_animal_types(client):
    response = client.get("api/v0/animaltypes")
    assert response.status_code == 200, "Happy Path, should return okay"
    assert len(response.json) == 1

def test_get_animal_type_by_id(client):
    response = client.get("api/v0/animaltypes/1")
    assert response.status_code == 200, "Happy Path, should return okay"
    assert "animalType" in response.json.keys(), "JSON body is not empty, key is in camelCase"

def test_get_non_prestent_animal_type(client):
    response = client.get("api/v0/animaltypes/99")
    assert response.status_code == 404, "Not present, throw 404 Error"

def test_post_new_animal_type_happy_path(client):
    response = client.post("api/v0/animaltypes", json={"animalType":"cat"})
    assert response.status_code == 201, "New animal type was successfully created"

@pytest.mark.parametrize(
        ("data",),
        (
            ({"animalType":"cat", "animalTypeId": 99},), # animalTypeId is not allowed in post requests
            ({"animalType":"dog"},), # anmial_type has to be unique
            ({"animal_type":"cat"},), # key has to be in camelCase
            ({"animalType":1},), # value has to be a string
            ({"myType":"lizard", "animalType":"lizard"},), # reject unkown keys
        ),
)
def test_post_with_malformed_body_is_rejected(client, data):
    response = client.post("api/v0/animaltypes", json=data)
    assert response.status_code == 400, "Throw bad request error"
