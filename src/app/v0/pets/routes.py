import sqlalchemy as sa
from apifairy import body, other_responses, response, authenticate
from flask import Blueprint, request, abort
from ..auth.auth import token_auth

from app import db
from app.models import Pets

from ..schemas import EmptySchema
from .schemas import PetSchema

pets = Blueprint("pets", __name__)
single_schema = PetSchema()
collection_schema = PetSchema(many=True)
update_schema = PetSchema(partial=True)
ResourceModel = Pets


@pets.get("/<int:id>")  # type: ignore
@authenticate(token_auth)
@response(single_schema)
@other_responses({404: "Pet not found"})
def get_by_id(id):
    """Returns a Pets object requested by id"""
    return db.get_or_404(ResourceModel, id)


@pets.get("/")  # type: ignore
@authenticate(token_auth)
@response(collection_schema)
def get_collection():
    """Return a collection of Pets objects if present"""
    return db.session.scalars(sa.select(ResourceModel)).all()


@pets.post("/")  # type: ignore
@authenticate(token_auth)
@body(single_schema)
@response(single_schema, 201)
@other_responses({400: "Invalid request body"})
def create(args):
    """Creates and saves a new Pets Object"""
    user = token_auth.current_user()
    if user:
        args["owner_id"] = user.user_id
        resource = ResourceModel(**args)
        db.session.add(resource)
        db.session.commit()
        return resource
    abort(401)


@pets.put("/<int:id>")  # type: ignore
@authenticate(token_auth)
@body(single_schema)
@response(single_schema)
@other_responses({400: "Invalid request body", 404: "Pet not found"})
def update(args, id):
    resource = db.get_or_404(ResourceModel, id)
    single_schema.load(request.json, instance=resource)
    db.session.commit()
    return resource


@pets.patch("/<int:id>")  # type: ignore
@authenticate(token_auth)
@body(update_schema)
@response(single_schema)
@other_responses({400: "Invalid request body", 404: "Pet not found"})
def update_partial(args, id):
    resource = db.get_or_404(ResourceModel, id)
    update_schema.load(request.json, instance=resource)
    db.session.commit()
    return resource


@pets.delete("/<int:id>")  # type: ignore
@authenticate(token_auth)
@response(EmptySchema, 204)
@other_responses({404: "Pet not found"})
def delete(id):
    db.get_or_404(ResourceModel, id)
    db.session.execute(sa.delete(ResourceModel).where(ResourceModel.pet_id == id))
    db.session.commit()


@pets.patch("/<int:id>/borrow")  # type: ignore
@authenticate(token_auth)
@body(EmptySchema)
@response(single_schema)
@other_responses({400: "Invalid request body", 404: "Pet not found"})
def borrow(args, id):
    resource = db.get_or_404(ResourceModel, id)
    resource.borrower_id
    db.session.commit()
    return resource


@pets.patch("/<int:id>/return")  # type: ignore
@authenticate(token_auth)
@body(EmptySchema)
@response(single_schema)
@other_responses({400: "Invalid request body", 404: "Pet not found"})
def return_pet(args, id):
    resource = db.get_or_404(ResourceModel, id)
    resource.borrower_id = None
    db.session.commit()
    return resource
