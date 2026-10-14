import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    DATABASE_USER=os.environ.get('DATABASE_USER')
    DATABASE_PASSWORD=os.environ.get('DATABASE_PASSWORD')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
