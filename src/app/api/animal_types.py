import sqlalchemy as sa
from app import db
from app.models import AnimalTypes
from app.api import bp

@bp.get("/animaltypes")
def get_animal_type_collection()->list[dict]:
    """Return a collection of animal types"""
    animal_types = db.session.scalars(sa.select(AnimalTypes)).all()
    return [
        {
            "animalTypeId": animal_type.animal_type_id,
            "animalType": animal_type.animal_type,
        }
        for animal_type in animal_types
    ]
