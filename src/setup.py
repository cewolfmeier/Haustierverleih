"""Setup script for new installations"""

#!/usr/bin/env python3
from app.models import Roles, Users
import secrets
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def create_password():
    password = secrets.token_hex()
    print("User 'root' initial Password: ", password)
    print("It is highly recommended to change this after first login.")
    return password


def setup_data():
    with app.app_context():
        roles = [
            Roles(role_id=1, role="admin"),
            Roles(role_id=2, role="user"),
        ]

        db.session.add_all(roles)
        db.session.commit()
        print("Roles created successfully!")

        root_user = Users(
            username="root", role_id=1
        )
        root_user.set_password(create_password())

        db.session.add(root_user)
        db.session.commit()
        print("root created successfully!")


if __name__ == "__main__":
    setup_data()
