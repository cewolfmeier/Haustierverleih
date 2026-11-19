def test_get_animal_types(client):
    response = client.get("api/v0/animaltypes")
    assert response.status_code == 200, "Happy Path, should return okay"
    assert response.json == []
