from marshmallow_sqlalchemy import auto_field

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
    borrower = auto_field("borrowed", dump_only=True)
    owner = auto_field("owned", dump_only=True)
    animal_type = auto_field(dump_only=True)
