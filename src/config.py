import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
default_user_upload_dir = os.path.join(basedir, 'app/static/images/user_uploads')

class Config:
    APIFAIRY_TITLE="Haustierverleih API"
    APIFAIRY_VERSION="0.0.0"
    DATABASE_USER=os.environ.get('DATABASE_USER')
    DATABASE_PASSWORD=os.environ.get('DATABASE_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle' : 280}
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = (os.environ.get('UPLOAD_FOLDER') 
                     or os.mkdir(default_user_upload_dir) 
                     if not os.path.exists(default_user_upload_dir) 
                     else default_user_upload_dir)
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 2 * 1000 * 1000 # Limit Uploads to 2 Megabyte