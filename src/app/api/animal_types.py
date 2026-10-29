from flask import request
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
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

@bp.post("/animaltypes")
def add_new_animal_type()->tuple[dict, int]:
    """Return a collection of animal types"""
    new_animal_type = AnimalTypes(
        animal_type = request.json["animalType"]
    )
    try:
        db.session.add(new_animal_type)
        db.session.commit()
    except IntegrityError:
        return {}, 400
    return {
            "animalTypeId": new_animal_type.animal_type_id,
            "animalType": new_animal_type.animal_type,
        }, 201
