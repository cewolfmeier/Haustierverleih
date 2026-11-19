import sqlalchemy as sa
from apifairy import body, other_responses, response
from flask import abort, request

from app import db
from app.models import AnimalTypes
from app.v0 import bp

from ..schemas import EmptySchema
from .schemas import AnimalTypeSchema

single_schema = AnimalTypeSchema()
collection_schema = AnimalTypeSchema(many=True)
ResourceModel = AnimalTypes


@bp.get("animaltypes/<int:id>")  # type: ignore
@response(single_schema)
@other_responses({404: "Animal type not found"})
def get_animal_type_by_id(id):
    """Returns an AnimalTypes object requested by id"""
    return db.get_or_404(ResourceModel, id)


@bp.get("/animaltypes")  # type: ignore
@response(collection_schema)
def get_animal_type_collection():
    """Return a collection of AnimalTypes objects if present"""
    return db.session.scalars(sa.select(ResourceModel)).all()


@bp.post("/animaltypes")  # type: ignore
@body(single_schema)
@response(single_schema, 201)
@other_responses({400: "Invalid request body"})
def create_animal_type(args):
    """Creates and saves a new AnimalType Object"""
    if db.session.scalar(
        sa.select(ResourceModel).where(ResourceModel.animal_type == args.get("animal_type"))
    ):
        abort(400)
    resource = ResourceModel(**args)
    db.session.add(resource)
    db.session.commit()
    return resource


# Same route for put and patch, because currently only one property can be changed
@bp.route("/animaltypes/<int:id>", methods=["PUT", "PATCH"])  # type: ignore
@body(single_schema)
@response(single_schema, 200)
@other_responses({400: "Invalid request body", 404: "Animal type not found"})
def update_animal_type(args, id):
    resource = db.get_or_404(ResourceModel, id)
    if db.session.scalar(
        sa.select(ResourceModel).where(ResourceModel.animal_type == args.get("animal_type"))
    ):
        abort(400)
    single_schema.load(request.json, instance=resource)
    db.session.commit()
    return resource


@bp.delete("/animaltypes/<int:id>")  # type: ignore
@response(EmptySchema, 204)
@other_responses({404: "Animal type not found"})
def delete_animal_type(id):
    db.get_or_404(ResourceModel, id)
    db.session.execute(sa.delete(ResourceModel).where(ResourceModel.animal_type_id == id))
    db.session.commit()
