import sqlalchemy as sa
from apifairy import body, other_responses, response, authenticate
from flask import Blueprint, request, abort
from ..auth.auth import token_auth

from app import db

from ..users.schemas import UserSchema

me = Blueprint("me", __name__)
me_schema = UserSchema()


@me.get("/")  # type: ignore
@authenticate(token_auth)
@response(me_schema)
def get_me():
    """Returns the current user"""
    return token_auth.current_user()
