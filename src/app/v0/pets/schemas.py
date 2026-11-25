from marshmallow_sqlalchemy import auto_field
from marshmallow.fields import Integer

from app import ma
from app.models import Pets

from ..schemas import CamelCaseSchema


class PetSchema(ma.SQLAlchemySchema, CamelCaseSchema):
    class Meta:
        model = Pets

    pet_id = auto_field(dump_only=True)
    name = auto_field()
    description = auto_field()
    image = auto_field(required=False)
    animal_type_id = auto_field()
    owner_id = auto_field(dump_only=True)
    borrower_id = auto_field(dump_only=True)
