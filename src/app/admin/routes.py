from functools import wraps

import sqlalchemy as sa
from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app import db
from app.admin import bp
from app.models import AnimalTypes, Pets, Roles, Users


# ---- DECORATORS AND GLOBAL FUNCTIONS ---- #
# This decorator was taken from the official Flask documentation
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not "current_user" in session:
            return redirect(url_for("auth.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not "admin" in session["current_user"]["role"]:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


# ---- ROUTES ---- #
@bp.route("/admin")
@login_required
@admin_required
def admin():
    """Admin-Bereich"""
    animal_types = db.session.scalars(sa.select(AnimalTypes)).all()
    users = db.session.scalars(sa.select(Users)).all()
    return render_template(
        "admin/admin.html",
        users=users,
        current_user=session["current_user"],
        animal_types=animal_types,
    )


# --- USER ADMINISTRATION --- #
@bp.get("/admin/user/<int:user_id>/edit")
@login_required
def get_edit_user(user_id):
    user = db.session.scalar(sa.select(Users).where(Users.user_id == user_id))
    roles = db.session.scalars(sa.select(Roles)).all()
    if user is None:
        abort(404)
    if (
        user.user_id != session["current_user"]["user_id"]
        and session["current_user"]["role"] != "admin"
    ):
        abort(403)
    return render_template(
        "admin/edit_user.html",
        user=user,
        roles=roles,
        current_user=session["current_user"],
    )


@bp.post("/admin/user/<int:user_id>/edit")
@login_required
def post_edit_user(user_id):
    user = db.session.scalar(sa.select(Users).where(Users.user_id == user_id))
    if user is None:
        abort(404)
    if (
        user.user_id != session["current_user"]["user_id"]
        and session["current_user"]["role"] != "admin"
    ):
        abort(403)
    # -- FORM VALIDATION -- #
    if user.user_id == session["current_user"]["user_id"]:
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        new_password_repeat = request.form.get("new_password_repeat")
        if (
            user.check_password(current_password)
            and new_password == new_password_repeat
        ):
            user.set_password(new_password)
    else:
        role_id = request.form.get("roles")
        role = db.session.scalar(sa.select(Roles).where(Roles.role_id == role_id))
        # check if at least one required field is not filled
        if role is None:
            flash("Ungültige Eingabe!", "error")
            return redirect(url_for("admin.get_edit_user", user_id=user_id))
        else:
            user.role_id = role_id
    db.session.commit()
    flash("Der Benutzer wurde erfolgreich aktualisiert.", "success")
    return redirect(url_for("admin.admin"))


@bp.route("/admin/user/<int:user_id>/delete")
@login_required
@admin_required
def delete_user(user_id):
    """Leer; wird zum Löschen eines Benutzers benötigt"""
    user = db.session.scalar(sa.select(Users).where(Users.user_id == user_id))
    if user is None:
        flash("Dieser Benutzer existiert nicht.", "error")
        abort(404)
    elif session["current_user"]["role"] == "user":
        flash("Du darfst keine Benutzer löschen", "error")
        abort(400)
    pets = db.session.scalars(sa.select(Pets).where(Pets.owner_id == user_id))
    for pet in pets:
        pet.delete_image(current_app.config["UPLOAD_FOLDER"])
    db.session.delete(user)
    db.session.commit()
    flash("Der Benutzer wurde erfolgreich gelöscht.", "success")
    return redirect(url_for("admin.admin"))


# --- ANIMAL TYPE ADMINISTRATION --- #
@bp.get("/admin/animal_type/new")
@login_required
@admin_required
def get_new_animal_type():
    return render_template(
        "admin/new_animal_type.html",
        current_user=session["current_user"],
    )


@bp.post("/admin/animal_type/new")
@login_required
@admin_required
def post_new_animal_type():
    name = request.form.get("name")
    # check if at least one required field is not filled
    if name == "":
        flash("Ungültige Eingabe!", "error")
    else:
        animal_type = AnimalTypes(animal_type=name)
        db.session.add(animal_type)
        db.session.commit()
        flash("Eine neue Tierart wurde erfolgreich angelegt.", "success")
        return redirect(url_for("admin.admin"))
    return redirect(url_for("admin.get_new_animal_type"))


@bp.get("/admin/animal_type/<int:animal_type_id>/edit")
@login_required
@admin_required
def get_edit_animal_type(animal_type_id):
    """Route für die Bearbeitung von Tierarten"""
    animal_type = db.session.scalar(
        sa.select(AnimalTypes).where(AnimalTypes.animal_type_id == animal_type_id)
    )
    return render_template(
        "admin/edit_animal_type.html",
        animal_type=animal_type,
        current_user=session["current_user"],
    )


@bp.post("/admin/animal_type/<int:animal_type_id>/edit")
@login_required
@admin_required
def post_edit_animal_type(animal_type_id):
    """Route für die Bearbeitung von Tierarten"""
    animal_type = db.session.scalar(
        sa.select(AnimalTypes).where(AnimalTypes.animal_type_id == animal_type_id)
    )
    if request.method == "POST":
        name = request.form.get("name")
        # check if at least one required field is not filled
        if name == "":
            flash("Erwischt, du Schlauberger!")
        else:
            animal_type.animal_type = name
            db.session.commit()
            flash("Der Benutzer wurde erfolgreich aktualisiert.", "success")
            return redirect(url_for("admin.admin"))
    return redirect(
        url_for("admin.get_edit_animal_type", animal_type_id=animal_type_id)
    )
