from datetime import UTC, datetime, timedelta

from apifairy import authenticate, body, other_responses, response
from flask import Blueprint, abort, url_for
from werkzeug.http import dump_cookie

from app import db
from app.models import Users

from ..users.schemas import UserSchema
from .auth import basic_auth
from .schemas import TokenSchema

new_user_schema = UserSchema(only=("username", "password"))
user_schema = UserSchema()


auth = Blueprint("v0_auth", __name__)

token_schema = TokenSchema()


@auth.post("/register")  # type: ignore
@body(new_user_schema)
@response(user_schema, 201)
@other_responses({400: "Invalid request body"})
def register(new_user):
    """Creates and saves a new User Object"""
    user = Users(
        username=new_user.get("username"),  # type: ignore
    )
    user.set_password(new_user.get("password"))
    db.session.add(user)
    db.session.commit()
    return user


@auth.post("/login")  # type: ignore
@authenticate(basic_auth)
@response(TokenSchema, status_code=200)
@other_responses({400: "Invalid Credentials"})
def login():
    """login"""
    user: Users | None = basic_auth.current_user()
    if not user:
        abort(400)
    refresh_token_exp = datetime.now(UTC) + timedelta(days=7)

    return (
        user.issue_token(datetime.now(UTC) + timedelta(hours=1)),
        200,
        {
            "Set-Cookie": dump_cookie(
                "refresh_token",
                user.issue_token(refresh_token_exp),
                path=url_for("auth.login"),
                expires=refresh_token_exp,
                httponly=True,
            )
        },
    )
