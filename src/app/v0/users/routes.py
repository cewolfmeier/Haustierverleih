import sqlalchemy as sa
from apifairy import body, other_responses, response
from flask import request

from app import db
from app.models import Users
from app.v0 import bp

from ..schemas import EmptySchema
from .schemas import UserSchema

single_schema = UserSchema()
collection_schema = UserSchema(many=True)
update_schema = UserSchema(partial=True)
ResourceModel = Users


@bp.get("users/<int:id>")  # type: ignore
@response(single_schema)
@other_responses({404: "User not found"})
def get_user_by_id(id):
    """Returns a Users object requested by id"""
    return db.get_or_404(ResourceModel, id)


@bp.get("/users")  # type: ignore
@response(collection_schema)
def get_user_collection():
    """Return a collection of User objects if present"""
    return db.session.scalars(sa.select(ResourceModel)).all()


@bp.post("/register")  # type: ignore
@body(single_schema)
@response(single_schema, 201)
@other_responses({400: "Invalid request body"})
def register(args):
    """Creates and saves a new User Object"""
    resource = ResourceModel(**args)
    db.session.add(resource)
    db.session.commit()
    return resource


@bp.put("/users/<int:id>")  # type: ignore
@body(single_schema)
@response(single_schema)
@other_responses({400: "Invalid request body", 404: "User not found"})
def update_user(args, id):
    resource = db.get_or_404(ResourceModel, id)
    single_schema.load(request.json, instance=resource)
    db.session.commit()
    return resource


@bp.patch("/users/<int:id>")  # type: ignore
@body(update_schema)
@response(single_schema)
@other_responses({400: "Invalid request body", 404: "User not found"})
def update_partial_user(args, id):
    resource = db.get_or_404(ResourceModel, id)
    update_schema.load(request.json, instance=resource)
    db.session.commit()
    return resource


@bp.delete("/users/<int:id>")  # type: ignore
@response(EmptySchema, 204)
@other_responses({404: "User not found"})
def delete_user(id):
    db.get_or_404(ResourceModel, id)
    db.session.execute(sa.delete(ResourceModel).where(ResourceModel.user_id == id))
    db.session.commit()
