from app import ma
from app.models import Pets

from ..schemas import CamelCaseSchema


class PetSchema(ma.SQLAlchemySchema, CamelCaseSchema):
    class Meta:
        model = Pets

    pet_id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    description = ma.auto_field()
    image = ma.auto_field()
    animal_type = ma.auto_field()
    owner_id = ma.auto_field()
    borrower_id = ma.auto_field()
