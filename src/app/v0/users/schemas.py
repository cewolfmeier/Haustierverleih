from app import ma
from app.models import Users

from ..schemas import CamelCaseSchema


class UserSchema(ma.SQLAlchemySchema, CamelCaseSchema):
    class Meta:
        model = Users

    user_id = ma.auto_field(dump_only=True)
    username = ma.auto_field()
    password_hash = ma.auto_field(load_only=True)
    role_id = ma.auto_field(required=False)
