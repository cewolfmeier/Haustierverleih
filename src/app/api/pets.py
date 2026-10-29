import sqlalchemy as sa
from app import db
from app.models import Pets
from app.api import bp

@bp.get("/pets")
def get_pet_collection()->list[dict]:
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
            "borrowerId": pet.borrower_id
        }
        for pet in pets
    ]

@bp.get("/pets/<int:id>")
def get_pet_by_id()->dict:
    """Return a pet by id"""
    pet = db.get_or_404(Pets, id)
    return {
        "petId": pet.pet_id,
        "name": pet.name,
        "description": pet.description,
        "image": pet.image,
        "animalTypeId": pet.animal_type_id,
        "ownerId": pet.owner_id,
        "borrowerId": pet.borrower_id
    }