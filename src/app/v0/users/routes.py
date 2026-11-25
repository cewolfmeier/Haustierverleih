import sqlalchemy as sa
from apifairy import body, other_responses, response, authenticate
from flask import Blueprint, request
from ..auth.auth import token_auth

from app import db
from app.models import Users

from ..schemas import EmptySchema
from .schemas import UserSchema

users = Blueprint("users", __name__)
single_schema = UserSchema()
collection_schema = UserSchema(many=True)
update_schema = UserSchema(partial=True)
ResourceModel = Users


@users.get("/<int:id>")  # type: ignore
@authenticate(token_auth)
@response(single_schema)
@other_responses({404: "User not found"})
def get_by_id(id):
    """Returns a Users object requested by id"""
    return db.get_or_404(ResourceModel, id)


@users.get("")  # type: ignore
@authenticate(token_auth)
@response(collection_schema)
def get_collection():
    """Return a collection of User objects if present"""
    return db.session.scalars(sa.select(ResourceModel)).all()


@users.put("/<int:id>")  # type: ignore
@authenticate(token_auth)
@body(single_schema)
@response(single_schema)
@other_responses({400: "Invalid request body", 404: "User not found"})
def update(args, id):
    resource = db.get_or_404(ResourceModel, id)
    single_schema.load(request.json, instance=resource)
    db.session.commit()
    return resource


@users.patch("/<int:id>")  # type: ignore
@authenticate(token_auth)
@body(update_schema)
@response(single_schema)
@other_responses({400: "Invalid request body", 404: "User not found"})
def update_partial(args, id):
    resource = db.get_or_404(ResourceModel, id)
    update_schema.load(request.json, instance=resource)
    db.session.commit()
    return resource


@users.delete("/<int:id>")  # type: ignore
@authenticate(token_auth)
@response(EmptySchema, 204)
@other_responses({404: "User not found"})
def delete(id):
    db.get_or_404(ResourceModel, id)
    db.session.execute(sa.delete(ResourceModel).where(ResourceModel.user_id == id))
    db.session.commit()
