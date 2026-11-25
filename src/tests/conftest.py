import base64

import jwt
import pytest

from app import create_app, db
from app.models import AnimalTypes, Pets, Roles, Users
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory"
    SECRET_KEY= "MySuperSecretTestKey"


@pytest.fixture
def app():
    app = create_app(config_class=TestConfig)

    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add_all(
            [
                Roles(role_id=1, role="user"), # type: ignore
                Roles(role_id=2, role="admin"), # type: ignore
            ]
        )
        db.session.commit()
        testusers = [
            Users(
                user_id=1, # type: ignore
                username="admin", # type: ignore
                role_id=2, # type: ignore
            ),
            Users(
                user_id=2, # type: ignore
                username="test", # type: ignore
                role_id=1, # type: ignore
            ),
        ]
        for testuser in testusers:
            testuser.set_password("test")
        db.session.add_all(testusers)
        db.session.add_all(
            [
                AnimalTypes(animal_type_id=1, animal_type="dog"), # type: ignore
                AnimalTypes(animal_type_id=2, animal_type="fish"), # type: ignore
            ]
        )
        db.session.commit()
        db.session.add_all(
            [
                Pets(
                    pet_id=1, # type: ignore
                    animal_type_id=1, # type: ignore
                    name="bello", # type: ignore
                    description="Loves to play in mudd", # type: ignore
                    owner_id=1, # type: ignore
                ),
                Pets(
                    pet_id=2, # type: ignore
                    animal_type_id=2, # type: ignore
                    name="blubber", # type: ignore
                    description="easy to keep, likes to swim belly up", # type: ignore
                    owner_id=1, # type: ignore
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
                Roles(role_id=1, role="User"), # type: ignore
                Roles(role_id=2, role="Admin"), # type: ignore
            ]
        )
        db.session.commit()
        testuser = Users(
            user_id=1, # type: ignore
            username="test", # type: ignore
            role_id=1, # type: ignore
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

    @property
    def token(self):
        return jwt.encode(
            {
                "sub": "2",
                "name": "test",
            },
            TestConfig.SECRET_KEY,
            algorithm="HS256",
        )

    @property
    def admin_token(self):
        return jwt.encode(
            {
                "sub": "1",
                "name": "admin",
            },
            TestConfig.SECRET_KEY,
            algorithm="HS256",
        )


@pytest.fixture
def auth(client):
    return AuthActions(client)
