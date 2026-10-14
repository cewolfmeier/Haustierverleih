import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    DATABASE_USER=os.environ.get('DATABASE_USER')
    DATABASE_PASSWORD=os.environ.get('DATABASE_PASSWORD')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/images/user_uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 2 * 1000 * 1000 # Limit Uploads to 2 Megabyte