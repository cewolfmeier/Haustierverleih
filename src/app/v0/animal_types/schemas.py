from app import ma
from app.models import AnimalTypes

from ..schemas import CamelCaseSchema


class AnimalTypeSchema(ma.SQLAlchemySchema, CamelCaseSchema):
    class Meta:
        model = AnimalTypes

    animal_type_id = ma.auto_field(dump_only=True)
    animal_type = ma.auto_field()
