import sqlalchemy as sa
from apifairy import body, other_responses, response
from flask import abort, request

from app import db
from app.models import AnimalTypes
from app.v0 import bp

from ..schemas import EmptySchema
from .schemas import AnimalTypeSchema

animal_type_schema = AnimalTypeSchema()
animal_types_schema = AnimalTypeSchema(many=True)


@bp.get("animaltypes/<int:id>")  # type: ignore
@response(animal_type_schema)
@other_responses({404: "Animal type not found"})
def get_by_id(id):
    """Returns an AnimalTypes object requested by id"""
    return db.get_or_404(AnimalTypes, id)


@bp.get("/animaltypes")  # type: ignore
@response(animal_types_schema)
def get_collection():
    """Return a collection of AnimalTypes objects if present"""
    return db.session.scalars(sa.select(AnimalTypes)).all()


@bp.post("/animaltypes")  # type: ignore
@body(animal_type_schema)
@response(animal_type_schema, 201)
@other_responses({400: "Invalid request body"})
def create(args):
    """Creates and saves a new AnimalType Object"""
    if db.session.scalar(
        sa.select(AnimalTypes).where(AnimalTypes.animal_type == args.get("animal_type"))
    ):
        abort(400)
    animal_type = AnimalTypes(**args)
    db.session.add(animal_type)
    db.session.commit()
    return animal_type


# Same route for put and patch, because currently only one property can be changed
@bp.route("/animaltypes/<int:id>", methods=["PUT", "PATCH"])  # type: ignore
@body(animal_type_schema)
@response(animal_type_schema, 200)
@other_responses({400: "Invalid request body", 404: "Animal type not found"})
def update(args, id):
    animal_type = db.get_or_404(AnimalTypes, id)
    if db.session.scalar(
        sa.select(AnimalTypes).where(AnimalTypes.animal_type == args.get("animal_type"))
    ):
        abort(400)
    animal_type_schema.load(request.json, instance=animal_type)
    db.session.commit()
    return animal_type


@bp.delete("/animaltypes/<int:id>")  # type: ignore
@response(EmptySchema, 204)
@other_responses({404: "Animal type not found"})
def delete(id):
    db.get_or_404(AnimalTypes, id)
    db.session.execute(sa.delete(AnimalTypes).where(AnimalTypes.animal_type_id == id))
    db.session.commit()
