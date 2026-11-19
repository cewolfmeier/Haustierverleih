import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apifairy import APIFairy
import os


db = SQLAlchemy()
migrate = Migrate()
apifairy = APIFairy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    apifairy.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from app.v0 import bp as api_v0_bp
    app.register_blueprint(api_v0_bp, url_prefix="/api/v0")

    if not app.debug and not app.testing:
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/haustierverleih.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Haustierverleih startup')

    return app


from app import models
