from apifairy import authenticate, response
from flask import Blueprint

from ..auth.auth import token_auth
from ..users.schemas import UserSchema

me = Blueprint("me", __name__)
me_schema = UserSchema()


@me.get("/")  # type: ignore
@authenticate(token_auth)
@response(me_schema)
def get_me():
    """Returns the current user"""
    return token_auth.current_user()
