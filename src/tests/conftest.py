import pytest
from app import create_app, db
from app.models import Roles
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mariadb+mariadbconnector://hvtest:hvtest@127.0.0.1:3305/hvtest"


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

    yield app

    db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()