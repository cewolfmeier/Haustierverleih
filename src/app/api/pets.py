from flask import request, current_app
from werkzeug.utils import secure_filename
import uuid
import os
import sqlalchemy as sa
from app import db
from app.models import Pets
from app.api import bp

# ---- DECORATORS AND GLOBAL FUNCTIONS ---- #
# This function was taken from the official Flask documentation
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

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

@bp.post("/pets")
def create_pet()->tuple[dict, int]:
    """Return a pet by id"""
    filename = None
    if "image" in request.json:
        image = request.files["image"]
        if image.filename:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                filename = str(uuid.uuid4()) + "." + filename.rsplit('.', 1)[1].lower()
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    new_pet = Pets(
        name = request.json["name"],
        description = request.json["description"],
        animal_type_id = request.json["animalTypeId"],
        image = filename
        #Todo: Set Owner Id from current user
    )
    db.session.add(new_pet)
    db.session.commit()
    return {
        "petId": new_pet.pet_id,
        "name": new_pet.name,
        "description": new_pet.description,
        "image": new_pet.image,
        "animalTypeId": new_pet.animal_type_id,
        "ownerId": new_pet.owner_id,
        "borrowerId": new_pet.borrower_id
    }, 201
