from app.v0 import bp
from .schemas import AnimalTypeSchema

animal_type_schema = AnimalTypeSchema()
animal_types_schema = AnimalTypeSchema(many=True)

@bp.get("/animaltypes")
def get_animal_type_collection() -> list[dict]:
    """Return a collection of animal types"""
    return []
