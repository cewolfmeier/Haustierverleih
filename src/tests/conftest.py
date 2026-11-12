import pytest
from app import create_app, db
from app.models import Roles, Users
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
            ]
        )
        db.session.commit()

    yield app

    db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
