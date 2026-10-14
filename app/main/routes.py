from flask import render_template, redirect, request, url_for, flash, session, abort
from werkzeug.utils import secure_filename
from functools import wraps
import uuid
import os
import sqlalchemy as sa
from app import db
from app.models import Roles, Users, AnimalTypes, Pets
from app.main import bp

# ---- DECORATORS AND GLOBAL FUNCTIONS ---- #
# This function was taken from the official Flask documentation
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in bp.config['ALLOWED_EXTENSIONS']


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
# --- MAIN --- #
@bp.route("/")
@bp.route("/index")
@login_required
def index():
    """Startseite mit Liste aller Tiere"""
    pets = db.session.scalars(sa.select(Pets)).all()
    return render_template(
        'index.html', 
        pets=pets, 
        current_user=session['current_user'],
        )

@bp.route("/pet/<int:pet_id>")
@login_required
def pet(pet_id):
    """Zeigt die Details eines Tieres an"""
    pet = db.session.scalar(sa.select(Pets).where(Pets.pet_id == pet_id))
    if pet is None:
        abort(404)
    return render_template('pet.html', pet=pet, current_user=session['current_user'])


@bp.route("/pet/<int:pet_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_pet(pet_id):
    """Seite zum Bearbeiten eines Tieres"""
    animal_types = db.session.scalars(sa.select(AnimalTypes)).all()
    pet = db.session.scalar(sa.select(Pets).where(Pets.pet_id == pet_id))
    filename = None
    if request.method == 'POST':
        # -- FORM VALIDATION -- #
        name = request.form.get('Name')
        description = request.form.get('Beschreibung')
        animal_type_id = request.form.get('Tierart')
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != "":
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    filename = str(uuid.uuid4()) + "." + filename.rsplit('.', 1)[1].lower()
                    image.save(os.path.join(bp.config['UPLOAD_FOLDER'], filename))
                else:
                    flash("Das Bild konnte nicht hochgeladen werden.", "warning")
        # check required fields
        if name == "" or description == "":
            flash(
                "Einige Daten wurden nicht korrekt übertragen. Bitte erneut versuchen.", 
                "error",
                )
        # -- DATABASE HANDLING -- #
        else:
            pet.from_dict(
                {
                    "name" : name,
                    "description" : description,
                    "animal_type_id" : animal_type_id,
                }
            )
            if filename is not None:
                pet.delete_image(bp.config['UPLOAD_FOLDER'])
                pet.image = filename
            db.session.commit()
            flash(
                "Glückwunsch! Deine Änderungen wurde erfolgreich gespeichert.", 
                "success"
                )
            return redirect(url_for('main.pet', pet_id=pet_id))
    if pet is None or animal_types is None:
        abort(404)
    return render_template(
        'edit_pet.html',
        pet=pet,
        animal_types=animal_types, 
        current_user=session['current_user'],
        )


@bp.route("/pet/<int:pet_id>/delete")
@login_required
def delete_pet(pet_id):
    """Leer; wird zum Löschen eines Tieres benötigt"""
    pet = db.session.scalar(sa.select(Pets).where(Pets.pet_id == pet_id))
    if pet is None:
        flash("Dieses Haustier existiert nicht.", 'error')
        abort(404)
    elif pet.owner_id != session['current_user']['user_id']:
        flash("Du kannst nur deine eigenen Haustiere löschen.", 'error')
        abort(400)
    pet.delete_image(bp.config['UPLOAD_FOLDER'])
    db.session.delete(pet)
    db.session.commit()
    flash("Das Haustier wurde erfolgreich gelöscht.", 'success')
    return redirect(url_for('main.pet_management'))


@bp.route("/pet/<int:pet_id>/borrow")
@login_required
def borrow_pet(pet_id):
    """Leer; wird für das Ausleihen benötigt"""
    pet = db.session.scalar(sa.select(Pets).where(Pets.pet_id == pet_id))
    if pet is None:
        flash("Dieses Haustier existiert nicht.", 'error')
        abort(404)
    elif pet.owner_id == session['current_user']['user_id']:
        flash("Du kannst deine eigenen Haustiere nicht ausleihen.", 'error')
        abort(400)
    elif pet.borrower_id is not None:
        flash("Dieses Haustier ist bereits verliehen", 'error')
        abort(400)
    pet.borrower_id = session['current_user']['user_id']
    db.session.commit()
    flash("Du leihst jetzt dieses Haustier aus.", 'success')
    return redirect(url_for('main.pet', pet_id=pet_id))


@bp.route("/pet/<int:pet_id>/return")
@login_required
def return_pet(pet_id):
    """Leer; wird für das Zurückgeben benötigt"""
    pet = db.session.scalar(sa.select(Pets).where(Pets.pet_id == pet_id))
    if pet is None:
        flash("Dieses Haustier existiert nicht.", 'error')
        abort(404)
    elif pet.borrower_id != session['current_user']['user_id']:
        flash("Dieses Haustier kann von dir nicht zurückgegeben werden.", 'error')
        abort(400)
    pet.borrower_id = None
    db.session.commit()
    flash("Du hast das Haustier erfolgreich zurückgegeben.", 'success')
    return redirect(url_for('main.pet', pet_id=pet_id))


@bp.route("/pet-management")
@login_required
def pet_management():
    """Verwaltung eigener und geliehener Tiere"""
    owned_pets = db.session.scalars(
        sa.select(Pets).where(Pets.owner_id == session['current_user']['user_id'])
        ).all()
    borrowed_pets = db.session.scalars(
        sa.select(Pets).where(Pets.borrower_id == session['current_user']['user_id'])
        ).all()
    owned_pets_counter = len(owned_pets)
    borrowed_pets_counter = len(borrowed_pets)
    return render_template(
        'pet_management.html', 
        borrowed_pets=borrowed_pets, 
        owned_pets=owned_pets, 
        owned_pets_counter=owned_pets_counter, 
        borrowed_pets_counter=borrowed_pets_counter, 
        current_user=session['current_user'],
        )


@bp.route("/pet/new", methods=['GET', 'POST'])
@login_required
def new_pet():
    """Seite zum Anlegen neuer Tiere"""
    filename = None
    animal_types = db.session.scalars(sa.select(AnimalTypes)).all()
    if request.method == 'POST':
        # -- FORM VALIDATION -- #
        name = request.form.get('Name')
        description = request.form.get('Beschreibung')
        animal_type = request.form.get('Tierart')
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != "":
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    filename = str(uuid.uuid4()) + "." + filename.rsplit('.', 1)[1].lower()
                    image.save(os.path.join(bp.config['UPLOAD_FOLDER'], filename))
                else:
                    flash("Das Bild konnte nicht hochgeladen werden.", "warning")
        # check if at least one required field is not filled
        if name == "" or description == "" or animal_type == "":
            flash(
                "Einige Daten wurden nicht korrekt übertragen. Bitte erneut versuchen.",
                "error")
        # -- DATABASE HANDLING -- #
        else:
            pet = Pets(
                name = name, 
                description = description,
                animal_type_id = animal_type,
                owner_id = session['current_user']['user_id'],
                image = filename
                )
            db.session.add(pet)
            db.session.commit()
            flash(
                "Glückwunsch! Dein Haustier wurde erfolgreich gespeichert.", 
                'success'
            )
            return redirect(url_for('main.pet_management'))
    return render_template(
        'add_pet.html', 
        animal_types=animal_types, 
        current_user=session['current_user'],
        )