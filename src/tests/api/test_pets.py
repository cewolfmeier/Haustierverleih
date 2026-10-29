
BASE_URL = "api/v0"

def test_get_pets_collection(client):
    response = client.get("/".join([BASE_URL,"pets"]))
    assert response.status_code == 200, "Happy Path, returns okay"
    assert response.json == []

def test_get_pet_by_id(client):
    response = client.get("/".join([BASE_URL,"pets/1"]))
    assert response.status_code == 200, "Happy Path, returns okay"
    assert response.json == {}
