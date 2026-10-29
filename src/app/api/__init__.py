from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import pets, animal_types, users, me