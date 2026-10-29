from flask import request
import sqlalchemy as sa
from app import db
from app.models import Users
from app.api import bp

@bp.get("/users")
def get_users_collection()->list[dict]:
    """Returns a collection of users"""
    users = db.session.scalars(sa.select(Users)).all()
    return [
        {
            "userId": user.user_id,
            "username": user.username,
            "roleId": user.role_id,
        }
        for user in users
    ]

""" Note: Usually, one would register with an email with 
    an email-confirmation being sent to prevent 
    an attack by flooding the database with dummy users"""
@bp.post("/users")
def add_new_user()->tuple[dict, int]:
    """Adds a new user and returns a short ok message"""
    new_user = Users(
        username = request.json["username"],
        role_id = 1 #ToDo: Change to actual role id for lowest user privilege
        )
    new_user.set_password(request.json["password"])
    if db.session.scalar(sa.select(Users).where(Users.username == new_user.username)):
        return {"message": "user is already registered"}, 400
    db.session.add(new_user)
    db.session.commit()
    return {"message": "ok"}, 201
