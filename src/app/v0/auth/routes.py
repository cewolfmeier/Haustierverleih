from datetime import UTC, datetime, timedelta

import jwt
from apifairy import authenticate, body, other_responses, response
from flask import Blueprint, abort, after_this_request, current_app, request, url_for
from werkzeug.http import dump_cookie

from app import db
from app.models import Users

from ..schemas import EmptySchema
from ..users.schemas import UserSchema
from .auth import basic_auth, token_auth
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
        username=new_user.username,  # type: ignore
    )
    user.set_password(request.json.get("password"))
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
        {"access_token": user.issue_token(datetime.now(UTC) + timedelta(hours=1))},
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


@auth.put("/tokens")  # type: ignore
@response(TokenSchema, status_code=200)
@other_responses({401: "Invalid Token"})
def rotate_tokens():
    """login"""
    # ToDo: Manage refresh token in db
    try:
        claims = jwt.decode(
            (request.cookies.get("refresh_token") or ""),
            key=current_app.config["SECRET_KEY"],
            algorithms=[
                "HS256",
            ],
        )
        user = db.get_or_404(Users, claims.get("sub"))
        refresh_token_exp = datetime.now(UTC) + timedelta(days=7)
        return (
            {"access_token": user.issue_token(datetime.now(UTC) + timedelta(hours=1))},
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
    except jwt.PyJWTError:
        abort(401)


@auth.delete("/logout")  # type: ignore
@authenticate(token_auth)
@response(EmptySchema)
def delete():
    """Invalidates the refresh_token"""

    # ToDo: Manage refresh token in db
    # refresh_token = request.cookies.get("refresh_token")
    @after_this_request
    def clear_refresh_token_cookie(response):
        response.delete_cookie("refresh_token", path=url_for("auth.login"))
        return response

    return {}, 204
