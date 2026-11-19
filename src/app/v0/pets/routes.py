import sqlalchemy as sa
from apifairy import body, other_responses, response
from flask import abort, request

from app import db
from app.models import Pets
from app.v0 import bp

from ..schemas import EmptySchema
from .schemas import PetSchema

single_schema = PetSchema()
collection_schema = PetSchema(many=True)
update_schema = PetSchema(partial=True)
ResourceModel = Pets

@bp.get("pets/<int:id>")  # type: ignore
@response(single_schema)
@other_responses({404: "Animal type not found"})
def get_by_id(id):
    """Returns a Pets object requested by id"""
    return db.get_or_404(ResourceModel, id)


@bp.get("/pets")  # type: ignore
@response(collection_schema)
def get_collection():
    """Return a collection of Pets objects if present"""
    return db.session.scalars(sa.select(ResourceModel)).all()


@bp.post("/pets")  # type: ignore
@body(single_schema)
@response(single_schema, 201)
@other_responses({400: "Invalid request body"})
def create(args):
    """Creates and saves a new Pets Object"""
    if db.session.scalar(
        sa.select(ResourceModel).where(ResourceModel.animal_type == args.get("animal_type"))
    ):
        abort(400)
    animal_type = ResourceModel(**args)
    db.session.add(animal_type)
    db.session.commit()
    return animal_type


@bp.put("/pets/<int:id>")  # type: ignore
@body(single_schema)
@response(single_schema, 200)
@other_responses({400: "Invalid request body", 404: "Pet not found"})
def update(args, id):
    resource = db.get_or_404(ResourceModel, id)
    if db.session.scalar(
        sa.select(ResourceModel).where(ResourceModel.animal_type == args.get("animal_type"))
    ):
        abort(400)
    update_schema.load(request.json, instance=resource)
    db.session.commit()
    return resource


@bp.route("/pets/<int:id>")  # type: ignore
@body(update_schema)
@response(single_schema, 200)
@other_responses({400: "Invalid request body", 404: "Pet not found"})
def update_partial(args, id):
    resource = db.get_or_404(ResourceModel, id)
    if db.session.scalar(
        sa.select(ResourceModel).where(ResourceModel.animal_type == args.get("animal_type"))
    ):
        abort(400)
    update_schema.load(request.json, instance=resource)
    db.session.commit()
    return resource


@bp.delete("/pets/<int:id>")  # type: ignore
@response(EmptySchema, 204)
@other_responses({404: "Pet not found"})
def delete(id):
    db.get_or_404(ResourceModel, id)
    db.session.execute(sa.delete(ResourceModel).where(ResourceModel.pet_id == id))
    db.session.commit()
