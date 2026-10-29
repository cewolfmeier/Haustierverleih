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