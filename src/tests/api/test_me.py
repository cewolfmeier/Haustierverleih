def test_get_me(client, auth):
    response = client.get(
        "api/v0/me/", headers={"Authorization": "Bearer " + auth.token}
    )
    assert response.status_code == 200, "Happy Path, should return okay"
