from app.v0 import bp
from .schemas import AnimalTypeSchema
from apifairy import response
from app import db
import sqlalchemy as sa
from app.models import AnimalTypes

animal_type_schema = AnimalTypeSchema()
animal_types_schema = AnimalTypeSchema(many=True)

@bp.get("animaltypes/<int:id>") # type: ignore
@response(animal_type_schema)
def get_by_id(id):
    """Returns an AnimalTypes object requested by id"""
    return db.get_or_404(AnimalTypes, id)

@bp.get("/animaltypes")
@response(animal_types_schema)
def get_collection():
    """Return a collection of AnimalTypes objects if present"""
    return db.session.scalars(sa.select(AnimalTypes)).all()
