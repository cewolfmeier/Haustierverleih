from app.v0 import bp
from .schemas import AnimalTypeSchema
from apifairy import response, body, other_responses
from app import db
import sqlalchemy as sa
from app.models import AnimalTypes
from flask import abort

animal_type_schema = AnimalTypeSchema()
animal_types_schema = AnimalTypeSchema(many=True)

@bp.get("animaltypes/<int:id>") # type: ignore
@response(animal_type_schema)
def get_by_id(id):
    """Returns an AnimalTypes object requested by id"""
    return db.get_or_404(AnimalTypes, id)

@bp.get("/animaltypes") # type: ignore
@response(animal_types_schema)
def get_collection():
    """Return a collection of AnimalTypes objects if present"""
    return db.session.scalars(sa.select(AnimalTypes)).all()

@bp.post("/animaltypes") # type: ignore
@body(animal_type_schema)
@response(animal_type_schema, 201)
@other_responses({
    400: "invalid request body"
})
def create(args):
    """Creates and saves a new AnimalType Object"""
    if db.session.scalar(
        sa.select(AnimalTypes)
        .where(AnimalTypes.animal_type==args.get("animal_type"))
    ):
        abort(400)
    animal_type = AnimalTypes(**args)
    db.session.add(animal_type)
    db.session.commit()
    return animal_type
