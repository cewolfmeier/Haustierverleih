
BASE_URL = "api/v0"
def test_users(client):
    response = client.get("/".join([BASE_URL,"users"]))
    assert response.status_code == 200, "Happy Path, returns okay"
    assert response.json == []
