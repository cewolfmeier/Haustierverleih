from app.models import AnimalTypes
from app import marshmallow as ma

class AnimalTypeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = AnimalTypes

    animal_type_id = ma.auto_field()
    animal_type = ma.auto_field()
