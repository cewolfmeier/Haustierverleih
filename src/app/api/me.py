import sqlalchemy as sa

from app import db
from app.api import bp
from app.models import Pets, Users

from .auth import token_auth


@bp.get("/me")
@token_auth.login_required
def get_me() -> dict:
    """Returns the current user"""
    id = 1
    user = db.get_or_404(Users, id)  # ToDo: Get current user per decorator
    return {
        "userId": user.user_id,
        "username": user.username,
        "roleId": user.role_id,
    }


@bp.get("/me/pets")
@token_auth.login_required
def get_me_pets() -> list[dict]:
    """Returns a collection of pets for the current user"""
    id = 1
    pets = db.session.scalars(sa.select(Pets).where(Pets.owner_id == id)).all()
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


@bp.get("/me/pets/<int:id>")
@token_auth.login_required
def get_me_pets_by_id(id: int) -> dict:
    """Returns a pet by id for the current user"""
    pet = db.get_or_404(Pets, id)  # ToDo: Get current user per decorator
    return {
        "petId": pet.pet_id,
        "name": pet.name,
        "description": pet.description,
        "image": pet.image,
        "animalTypeId": pet.animal_type_id,
        "ownerId": pet.owner_id,
        "borrowerId": pet.borrower_id,
    }
