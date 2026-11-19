import sqlalchemy as sa

from app.v0 import bp
from app import db
from app.models import Users



@bp.get("/users")
def get_users_collection() -> list[dict]:
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