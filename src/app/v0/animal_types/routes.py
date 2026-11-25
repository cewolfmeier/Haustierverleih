import sqlalchemy as sa
from apifairy import body, other_responses, response, authenticate
from flask import Blueprint, abort, request
from ..auth.auth import token_auth

from app import db
from app.models import AnimalTypes

from ..schemas import EmptySchema
from .schemas import AnimalTypeSchema

animal_types = Blueprint("animal_types", __name__)
single_schema = AnimalTypeSchema()
collection_schema = AnimalTypeSchema(many=True)
ResourceModel = AnimalTypes


@animal_types.get("/<int:id>")  # type: ignore
@authenticate(token_auth, role="admin")
@response(single_schema)
@other_responses({404: "Animal type not found"})
def get_by_id(id):
    """Returns an AnimalTypes object requested by id"""
    return db.get_or_404(ResourceModel, id)


@animal_types.get("/")  # type: ignore
@authenticate(token_auth)
@response(collection_schema)
def get_collection():
    """Return a collection of AnimalTypes objects if present"""
    return db.session.scalars(sa.select(ResourceModel)).all()


@animal_types.post("/")  # type: ignore
@authenticate(token_auth, role="admin")
@body(single_schema)
@response(single_schema, 201)
@other_responses({400: "Invalid request body"})
def create(args):
    """Creates and saves a new AnimalType Object"""
    if db.session.scalar(
        sa.select(ResourceModel).where(
            ResourceModel.animal_type == args.get("animal_type")
        )
    ):
        abort(400)
    resource = ResourceModel(**args)
    db.session.add(resource)
    db.session.commit()
    return resource


# Same route for put and patch, because currently only one property can be changed
@animal_types.route("/<int:id>", methods=["PUT", "PATCH"])  # type: ignore
@authenticate(token_auth, role="admin")
@body(single_schema)
@response(single_schema, 200)
@other_responses({400: "Invalid request body", 404: "Animal type not found"})
def update(args, id):
    resource = db.get_or_404(ResourceModel, id)
    if db.session.scalar(
        sa.select(ResourceModel).where(
            ResourceModel.animal_type == args.get("animal_type")
        )
    ):
        abort(400)
    single_schema.load(request.json, instance=resource)
    db.session.commit()
    return resource


@animal_types.delete("/<int:id>")  # type: ignore
@authenticate(token_auth, role="admin")
@response(EmptySchema, 204)
@other_responses({404: "Animal type not found"})
def delete(id):
    db.get_or_404(ResourceModel, id)
    db.session.execute(
        sa.delete(ResourceModel).where(ResourceModel.animal_type_id == id)
    )
    db.session.commit()
