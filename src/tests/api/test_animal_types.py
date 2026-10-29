
BASE_URL = "api/v0"
def test_animal_types(client):
    response = client.get("/".join([BASE_URL,"animaltypes"]))
    assert response.status_code == 200, "Happy Path, returns okay"
    assert response.json == []
