from marshmallow.fields import String
from marshmallow_sqlalchemy import auto_field

from app import ma
from app.models import Users

from ..schemas import CamelCaseSchema


class UserSchema(ma.SQLAlchemySchema, CamelCaseSchema):
    class Meta:
        model = Users

    user_id = auto_field(dump_only=True)
    username = auto_field()
    password = String(load_only=True)
    role_id = auto_field(required=False)
