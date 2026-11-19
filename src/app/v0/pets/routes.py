import sqlalchemy as sa
from flask import current_app

from app import db
from app.models import Pets
from app.v0 import bp


# ---- DECORATORS AND GLOBAL FUNCTIONS ---- #
# This function was taken from the official Flask documentation
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


@bp.get("/pets")
def get_pet_collection() -> list[dict]:
    """Return a collection of pets"""
    pets = db.session.scalars(sa.select(Pets)).all()
    return [
        {
            "petId": pet.pet_id,
            "name": pet.name,
            "description": pet.description,
            "image": pet.image,
            "animalTypeId": pet.animal_type_id,
            "ownerId": pet.owner_id,
            "borrowerId": pet.borrower_id,
        }
        for pet in pets
    ]


@bp.get("/pets/<int:id>")
def get_pet_by_id(id) -> dict:
    """Return a pet by id"""
    pet = db.get_or_404(Pets, id)
    return {
        "petId": pet.pet_id,
        "name": pet.name,
        "description": pet.description,
        "image": pet.image,
        "animalTypeId": pet.animal_type_id,
        "ownerId": pet.owner_id,
        "borrowerId": pet.borrower_id,
    }
