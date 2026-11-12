def test_get_me(client):
    response = client.get("api/v0/me")
    assert response.status_code == 200, "Happy Path, returns okay"
    assert response.json == {}


def test_get_my_pets(client):
    response = client.get("api/v0/me/pets")
    assert response.status_code == 200, "Happy Path, returns okay"
    assert response.json == []


def test_get_my_pets_by_id(client):
    response = client.get("api/v0/me/pets/1")
    assert response.status_code == 200, "Happy Path, returns okay"
    assert response.json == {}
