from datetime import UTC, datetime, timedelta

import jwt
import sqlalchemy as sa
from flask import abort, current_app, make_response
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from app import db
from app.api import bp
from app.models import Users

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password) -> Users | None:
    username = username.lower()
    user = db.session.scalar(sa.select(Users).where(Users.username == username))
    if user and user.check_password(password):
        return user


@token_auth.verify_token
def verify_token(token):
    try:
        data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        user = db.session.scalar(
            sa.select(Users).where(Users.user_id == data.get("sub"))
        )
        return user if user else None
    except:
        return


@bp.post("/tokens")
@basic_auth.login_required
def create_tokens():
    user = basic_auth.current_user()
    if not user:
        abort(500)
    token = jwt.encode(
        {
            "sub": str(user.user_id),
            "name": user.username,
            "admin": user.role_id == 2,
            "exp": datetime.now(UTC) + timedelta(hours=1),
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    response = make_response(
        {
            "userId": user.user_id,
            "username": user.username,
            "isAdmin": user.role_id == 2,
        }
    )
    response.set_cookie("refresh_token", token)
    return response

@bp.delete("/tokens")
@token_auth.login_required
def delete_refresh_token():
    response = make_response()
    response.delete_cookie(key="refresh_token")
    return response
