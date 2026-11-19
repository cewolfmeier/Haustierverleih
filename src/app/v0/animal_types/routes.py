from app.v0 import bp

@bp.get("/animaltypes")
def get_animal_type_collection() -> list[dict]:
    """Return a collection of animal types"""
    return []
