
BASE_URL = "api/v0"
def test_pets(client):
    response = client.get("/".join([BASE_URL,"pets"]))
    assert response.status_code == 200