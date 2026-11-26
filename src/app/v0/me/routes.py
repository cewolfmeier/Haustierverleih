import sqlalchemy as sa
from apifairy import authenticate, body, other_responses, response
from flask import Blueprint, abort, after_this_request, request, url_for

from app import db
from app.models import Users

from ..auth.auth import token_auth
from ..schemas import EmptySchema
from ..users.schemas import UserSchema

me = Blueprint("me", __name__)
me_schema = UserSchema()
update_password_schema = UserSchema(only=("password_old", "password"))
update_username_schema = UserSchema(only=("username",))


@me.get("/")  # type: ignore
@authenticate(token_auth)
@response(me_schema)
def get_me():
    """Returns the current user"""
    return token_auth.current_user()


@me.patch("/password")  # type: ignore
@authenticate(token_auth)
@body(update_password_schema)
@response(EmptySchema)
@other_responses({400: "Invalid request body", 401: "unauthorized"})
def update_password(args):
    """Updates password of the current user"""
    user: Users | None = token_auth.current_user()
    if not user:
        abort(401)
    passwords = update_password_schema.load(request.json)
    if user.check_password(passwords.get("password_old")):
        user.set_password(passwords.get("password"))
        db.session.commit()
        return {}
    abort(400)


@me.patch("/username")  # type: ignore
@authenticate(token_auth)
@body(update_username_schema)
@response(me_schema)
@other_responses({400: "Invalid request body", 401: "unauthorized"})
def update_username(args):
    """Updates username of the current user"""
    user = token_auth.current_user()
    update_username_schema.load(request.json, instance=user)
    db.session.commit()
    return user


@me.delete("/")  # type: ignore
@authenticate(token_auth)
@response(EmptySchema)
def delete():
    """Deletes the current user"""
    user: Users | None = token_auth.current_user()
    if user:
        db.session.execute(sa.delete(Users).where(Users.user_id == user.user_id))
        db.session.commit()

        @after_this_request
        def clear_refresh_token_cookie(response):
            response.delete_cookie("refresh_token", path=url_for("auth.login"))
            return response

        return {}, 204
    abort(400)
