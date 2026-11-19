def test_get_animal_types(client):
    response = client.get("api/v0/animaltypes")
    assert response.status_code == 200, "Happy Path, should return okay"
    assert len(response.json) == 1

def test_get_animal_type_by_id(client):
    response = client.get("api/v0/animaltypes/1")
    assert response.status_code == 200, "Happy Path, should return okay"
    assert "animal_type" in response.json.keys()

def test_get_non_prestent_animal_type(client):
    response = client.get("api/v0/animaltypes/99")
    assert response.status_code == 404, "Not present, throw 404 Error"
