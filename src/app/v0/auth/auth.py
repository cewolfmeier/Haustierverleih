import jwt
import sqlalchemy as sa
from flask import current_app
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import check_password_hash

from app import db
from app.models import Users

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username: str, password: str) -> Users | None:
    user = db.session.scalar(
        sa.select(Users).where(Users.username == username.casefold().strip())
    )
    password_hash = user.password_hash if user else ""
    if user and check_password_hash(password_hash if password_hash else "", password):
        return user


@token_auth.verify_token
def verify_token(token):
    try:
        claims = jwt.decode(
            token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
        )
        user = db.session.scalar(
            sa.select(Users).where(Users.user_id == claims.get("sub"))
        )
        return user if user else None
    except jwt.PyJWTError:
        return False


@token_auth.get_user_roles
def get_user_roles(user: Users):
    return user.role.role if user.role else ""
