from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask import session

class Roles(db.Model):
    __tablename__ = "roles"
    role_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    role: so.Mapped[str] = so.mapped_column(sa.String(255), index=True, unique=True)

    users: so.WriteOnlyMapped['Users'] = so.relationship(back_populates='role')

    def __repr__(self):
        return '<Role {}>'.format(self.role)

class Users(db.Model):
    __tablename__ = "users"
    user_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(255), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))
    role_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Roles.role_id),index=True)

    role: so.Mapped[Roles] = so.relationship(back_populates='users')

    owned_pets: so.WriteOnlyMapped['Pets'] = so.relationship(
        back_populates='owned', 
        foreign_keys="Pets.owner_id",
        passive_deletes=True,
        cascade='all, delete',
        )
    borrowed_pets: so.WriteOnlyMapped['Pets'] = so.relationship(
        back_populates='borrowed', 
        foreign_keys="Pets.borrower_id",
        passive_deletes=True,
        )

    def __repr__(self):
        return self.username.capitalize()
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def login(self):
        username = self.username.capitalize()
        session['current_user'] = {
                'user_id':self.user_id,
                'username' : username,
                'role' : self.role.role,
                }


class AnimalTypes(db.Model):
    __tablename__ = "animal_types"
    animal_type_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    animal_type: so.Mapped[str] = so.mapped_column(sa.String(255), index=True,
                                                   unique=True)

    pets: so.WriteOnlyMapped['Pets'] = so.relationship(back_populates='animal_type')

    def __repr__(self):
        return '<Animal type {}>'.format(self.animal_type)
    

class Pets(db.Model):
    __tablename__ = "pets"
    pet_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(255), index=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(255), index=True)
    image: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    animal_type_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(AnimalTypes
                                                                    .animal_type_id)
                                                                    ,index=True)
    owner_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Users.user_id, ondelete='CASCADE')
                                                                    ,index=True)
    borrower_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Users.user_id, ondelete='SET NULL')
                                                                    ,index=True, nullable=True)
    
    animal_type: so.Mapped[AnimalTypes] = so.relationship(back_populates='pets')
    owned: so.Mapped[Users] = so.relationship(
        back_populates='owned_pets',
        foreign_keys="Pets.owner_id",
        )
    borrowed: so.Mapped[Users] = so.relationship(
        back_populates='borrowed_pets', 
        foreign_keys="Pets.borrower_id",
        )

    def __repr__(self):
        return '<Pet {}>'.format(self.name)
    
    def add_image(self, image, directory=None):
        self.image = image
    
    def delete_image(self, directory):
        if self.image is not None:
            os.remove(os.path.join(directory, self.image))
    
    def from_dict(self, data, new=False):
        """Method to set the attributes with data
        provided by an import file or a validated form"""
        for field in [
            "pet_id",
            "name", 
            "description", 
            "image", 
            "animal_type_id",
            "owner_id", 
            "borrower_id",
            ]:
            if field in data:
                setattr(self, field, data[field])
        if new:
            pass