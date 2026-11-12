import base64

headers = {"Authorization": "Basic " + base64.b64encode(b"test:test").decode("utf-8")}
invalid_user_header = {"Authorization": "Basic " + base64.b64encode(b"toast:test").decode("utf-8")}
invalid_password_header = {"Authorization": "Basic " + base64.b64encode(b"test:toast").decode("utf-8")}

def test_refuse_login_without_auth_header(client):
    response = client.post("api/v0/login")
    assert response.status_code == 401

def test_refuse_login_with_invalid_credentials(client):
    response = client.post("api/v0/login", headers=invalid_user_header)
    assert response.status_code == 401
    response = client.post("api/v0/login", headers=invalid_password_header)
    assert response.status_code == 401

def test_accept_login_with_auth_header(client):
    response = client.post("api/v0/login", headers=headers)
    assert response.status_code == 200
