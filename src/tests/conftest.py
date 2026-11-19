import base64

import pytest

from app import create_app, db
from app.models import Roles, Users, AnimalTypes
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory"


@pytest.fixture
def app():
    app = create_app(config_class=TestConfig)

    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add_all(
            [
                Roles(role_id=1, role="User"),
                Roles(role_id=2, role="Admin"),
            ]
        )
        db.session.commit()
        testuser = Users(
            user_id=1,
            username="test",
            role_id=1,
        )
        testuser.set_password("test")
        db.session.add_all(
            [
                testuser,
                AnimalTypes(
                    animal_type_id=1,
                    animal_type="dog"
                ),
                AnimalTypes(
                    animal_type_id=2,
                    animal_type="fish"
                ),
            ]
        )
        db.session.commit()

        yield app

        db.drop_all()

@pytest.fixture
def app_minimal():
    app = create_app(config_class=TestConfig)

    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add_all(
            [
                Roles(role_id=1, role="User"),
                Roles(role_id=2, role="Admin"),
            ]
        )
        db.session.commit()
        testuser = Users(
            user_id=1,
            username="test",
            role_id=1,
        )
        testuser.set_password("test")
        db.session.add_all(
            [
                testuser,
            ]
        )
        db.session.commit()

        yield app

        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def client_minimal(app_minimal):
    return app_minimal.test_client()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        credentials = base64.b64encode(f"{username}:{password}".encode()).decode(
            "utf-8"
        )
        headers = {"Authorization": "Basic " + credentials}
        self._client.post("api/v0/login", headers=headers)


@pytest.fixture
def auth(client):
    return AuthActions(client)
