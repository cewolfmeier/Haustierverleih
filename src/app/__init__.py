import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, supports_credentials=True)

    @app.before_request
    def inject_bearer_from_cookie():
        """helper for HTTPTokenAuth
        The JWT is saved in a cookie. To use HTTPTokenAuth,
        the token has to be in a Bearer beader.
        """
        token = request.cookies.get("refresh_token")
        if token:
            request.environ["HTTP_AUTHORIZATION"] = f"Bearer {token}"

    from app.api import bp as api_bp

    app.register_blueprint(api_bp, url_prefix="/api/v0")

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


from app import models
