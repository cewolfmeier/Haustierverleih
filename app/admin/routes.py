from flask import render_template, redirect, request, url_for, flash, session, abort
from functools import wraps
import sqlalchemy as sa
from app import db
from app.models import Roles, Users, AnimalTypes, Pets
from app.admin import bp

# ---- DECORATORS AND GLOBAL FUNCTIONS ---- #
# This decorator was taken from the official Flask documentation
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'current_user' in session:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'admin' in session['current_user']['role']:
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
        'admin/admin.html', 
        users=users, 
        current_user=session['current_user'],
        animal_types=animal_types,
        )


@bp.route("/admin/user/<int:user_id>/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """Bearbeiten eines Benutzers"""
    user = db.session.scalar(sa.select(Users).where(Users.user_id == user_id))
    roles = db.session.scalars(sa.select(Roles)).all()
    if request.method == 'POST':
        role_id = request.form.get('roles')
        # check if at least one required field is not filled
        if role_id == "":
            flash("Erwischt, du Schlauberger!")
        else:
            user.role_id = role_id
            db.session.commit()
            flash(
                "Der Benutzer wurde erfolgreich aktualisiert.", 
                'success'
            )
            return redirect(url_for('auth.admin'))
    return render_template(
        'admin/edit_user.html', 
        user=user,
        roles= roles,
        current_user=session['current_user'],
        )


@bp.route("/admin/user/<int:user_id>/delete", methods=['GET', 'POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Leer; wird zum Löschen eines Benutzers benötigt"""
    user = db.session.scalar(sa.select(Users).where(Users.user_id == user_id))
    if user is None:
        flash("Dieser Benutzer existiert nicht.", 'error')
        abort(404)
    elif session['current_user']['role'] == "user":
        flash("Du darfst keine Benutzer löschen", 'error')
        abort(400)
    pets = db.session.scalars(sa.select(Pets).where(Pets.owner_id == user_id))
    for pet in pets:
        pet.delete_image(bp.config['UPLOAD_FOLDER'])
    db.session.delete(user)
    db.session.commit()
    flash("Der Benutzer wurde erfolgreich gelöscht.", 'success')
    return redirect(url_for('admin.admin'))


@bp.route("/admin/animal_type/new", methods=['GET', 'POST'])
@login_required
@admin_required
def new_animal_type():
    """Route für neue Tierarten"""
    if request.method == 'POST':
        name = request.form.get('name')
        # check if at least one required field is not filled
        if name == "":
            flash("Erwischt, du Schlauberger!")
        else:
            animal_type = AnimalTypes(animal_type=name)
            db.session.add(animal_type)
            db.session.commit()
            flash(
                "Glückwunsch! Eine neue Tierart wurde erfolgreich angelegt.", 
                'success'
            )
            return redirect(url_for('admin.admin'))
    return render_template(
        'admin/new_animal_type.html',
        current_user=session['current_user'],)


@bp.route("/admin/animal_type/<int:animal_type_id>/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def edit_animal_type(animal_type_id):
    """Route für die Bearbeitung von Tierarten"""
    animal_type = db.session.scalar(
        sa.select(AnimalTypes)
        .where(AnimalTypes.animal_type_id == animal_type_id)
        )
    if request.method == 'POST':
        name = request.form.get('name')
        # check if at least one required field is not filled
        if name == "":
            flash("Erwischt, du Schlauberger!")
        else:
            animal_type.animal_type = name
            db.session.commit()
            flash(
                "Der Benutzer wurde erfolgreich aktualisiert.", 
                'success'
            )
            return redirect(url_for('admin.admin'))
    return render_template(
        'admin/edit_animal_type.html',
        animal_type=animal_type,
        current_user=session['current_user'],)
