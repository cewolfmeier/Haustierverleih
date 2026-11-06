from flask import request, current_app, make_response
import sqlalchemy as sa
from app import db
from app.api import bp
from app.models import Users
from datetime import datetime, timezone, timedelta
import jwt
from functools import wraps
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('jwt_token')

        if not token:
            return {'msg': 'token.missing'}, 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return {'msg': 'token.invalid'}, 401

        return f(current_user, *args, **kwargs)

    return decorated

@bp.post("/login")
def login():
    username = request.form.get('Username')
    password = request.form.get('Password')
    if not username or not password:
        return {"msg": "form.missingData"}, 401
    username = username.lower()
    user = db.session.scalar(
        sa.select(Users).where(Users.username == username)
    )
    # -- LOGIN HANDLING -- #
    if user is None or not user.check_password(password):
        return {"msg": "login.wrongCredentials"}, 401
    user.login()
    token = jwt.encode(
        {
            'public_id': user.user_id, 
            'exp': datetime.now(timezone.utc) + timedelta(hours=1)
        },
        current_app.config['SECRET_KEY'], 
        algorithm="HS256"
    )

    response = make_response({"msg": "login.success"})
    response.set_cookie('jwt_token', token)
    return response, 200
