from marshmallow.fields import String

from app.v0.schemas import CamelCaseSchema


class TokenSchema(CamelCaseSchema):
    access_token = String()
