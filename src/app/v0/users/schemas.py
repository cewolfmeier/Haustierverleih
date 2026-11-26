import sqlalchemy as sa
from marshmallow import ValidationError, validates
from marshmallow.fields import String
from marshmallow_sqlalchemy import auto_field

from app import db, ma
from app.models import Users

from ..schemas import CamelCaseSchema


class UserSchema(ma.SQLAlchemySchema, CamelCaseSchema):
    class Meta:
        model = Users
        load_instance = True

    user_id = auto_field(dump_only=True)
    username = auto_field()
    password = String(load_only=True, required=True)
    password_old = String(load_only=True, required=True)
    role_id = auto_field(required=False)
    role = auto_field()

    @validates("username")
    def validate_username(self, value, **kwargs) -> ValidationError | None:
        if not self.instance or value == self.instance.username:
            return
        if len(value) == 0 or db.session.scalar(
            sa.select(Users).where(Users.username == value)
        ):
            raise ValidationError("Use a different name.")
