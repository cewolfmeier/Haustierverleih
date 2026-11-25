import logging
import os
from logging.handlers import RotatingFileHandler

from apifairy import APIFairy
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
apifairy = APIFairy()
ma = Marshmallow()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    apifairy.init_app(app)
    ma.init_app(app)

    # from app.errors import bp as errors_bp
    # app.register_blueprint(errors_bp)

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp)

    from app.admin import bp as admin_bp

    app.register_blueprint(admin_bp)

    from app.v0.auth.routes import auth as api_v0_auth

    app.register_blueprint(api_v0_auth, url_prefix="/api/v0")

    from app.v0.animal_types.routes import animal_types as api_v0_animal_types

    app.register_blueprint(api_v0_animal_types, url_prefix="/api/v0/animaltypes")

    from app.v0.pets.routes import pets as api_v0_pets

    app.register_blueprint(api_v0_pets, url_prefix="/api/v0/pets")

    from app.v0.users.routes import users as api_v0_users

    app.register_blueprint(api_v0_users, url_prefix="/api/v0/users")

    from app.v0.me.routes import me as api_v0_me

    app.register_blueprint(api_v0_me, url_prefix="/api/v0/me")

    if not app.debug and not app.testing:

        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler(
            "logs/haustierverleih.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s " "[in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Haustierverleih startup")

    return app
