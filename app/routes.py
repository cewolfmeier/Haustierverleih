from app import app
from flask import render_template, redirect, request, url_for, flash, session, abort
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import uuid
import os

# ---- DECORATORS AND GLOBAL FUNCTIONS ---- #
def get_db_connection(): 
    connection = mysql.connector.connect( 
        host="localhost", 
        user=app.config['DATABASE_USER'], 
        password=app.config['DATABASE_PASSWORD'], 
        database="haustierverleih" 
        ) 
    return connection

# This function was taken from the official Flask documentation
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# This decorator was taken from the official Flask documentation
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'current_user' in session:
            return redirect(url_for('login', next=request.url))
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
# --- AUTHENTICATION --- #
@app.route("/login", methods=['GET', 'POST'])
def login():
    """Login-Seite"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')
        # check if at least one required field is not filled
        if username == "" or password == "":
            flash("Bitte gib deine Anmeldedaten ein.", 'error')
        cursor.execute(f'''SELECT *
                    FROM users
                    INNER JOIN roles ON roles.role_id = users.role_id
                    WHERE username = %s
                   ''', (username,))
        user = cursor.fetchone()
        if user is None or not check_password_hash(user['password_hash'], password):
            flash("Die Anmeldedaten stimmen nicht überein", 'error')
        else:
            flash(
                "Anmeldung erfolgreich.", 
                'success'
            )
            session['current_user'] = user
            return redirect(url_for('index'))
    connection.close()
    return render_template('auth/login.html', current_user=None)


@app.route("/register", methods=['GET', 'POST'])
def register():
    """Seite zur Account-Erstellung"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('''SELECT role_id FROM roles
                   WHERE role = "user"''')
    role_id_user = cursor.fetchone()
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')
        password_repeat = request.form.get('Password-Repeat')
        # check if at least one required field is not filled
        if username == "" or password == "" or password_repeat == "":
            flash("Netter Versuch, so klappt das aber nicht.", 'error')
        elif password != password:
            flash("Die Passworteingabe stimmt nicht überein", 'error')
        else:
            cursor.execute('''
                           INSERT INTO users 
                           (username, password_hash, role_id) 
                           VALUES (%s, %s, %s)''', 
                           (username, generate_password_hash(password), role_id_user['role_id'])) 
            connection.commit() 
            flash(
                "Glückwunsch! Du bist jetzt registriert.", 
                'success'
            )
            cursor.execute(f'''SELECT *
                    FROM users
                    INNER JOIN roles ON roles.role_id = users.role_id
                    WHERE username = %s
                   ''', (username,))
            user = cursor.fetchone()
            connection.close()
            session['current_user'] = user
            return redirect(url_for('index'))
    connection.close()
    return render_template('auth/register.html', current_user=None)


@app.route("/logout")
@login_required
def logout():
    """Leer; wird für den Logout benötigt"""
    session.pop('current_user', None)
    return redirect(url_for('login', next=request.url))


# --- MAIN --- #
@app.route("/")
@app.route("/index")
@login_required
def index():
    """Startseite mit Liste aller Tiere"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f'''SELECT *
                    FROM pets
                    INNER JOIN animal_types 
                       ON pets.animal_type_id = animal_types.animal_type_id
                    INNER JOIN users ON pets.owner_id = user_id
                   ''')
    pets = cursor.fetchall()
    connection.close()
    return render_template(
        'index.html', 
        pets=pets, 
        current_user=session['current_user'],
        )

@app.route("/pet/<int:pet_id>")
@login_required
def pet(pet_id):
    """Zeigt die Details eines Tieres an"""
    pet = None
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f'''SELECT * 
                FROM pets
                INNER JOIN animal_types 
                    ON pets.animal_type_id = animal_types.animal_type_id
                INNER JOIN users
                        ON pets.owner_id = users.user_id
                WHERE pets.pet_id = {pet_id}''')
    pet = cursor.fetchone()
    connection.close()
    if pet is None:
        abort(404)
    return render_template('pet.html', pet=pet, current_user=session['current_user'])


@app.route("/pet/<int:pet_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_pet(pet_id):
    """Seite zum Bearbeiten eines Tieres"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('''SELECT * FROM animal_types''')
    animal_types = cursor.fetchall()
    if request.method == 'POST':
        name = request.form.get('Name')
        description = request.form.get('Beschreibung')
        animal_type_id = request.form.get('Tierart')
        # check if at least one required field is not filled
        if name == "" or description == "":
            flash(
                "Einige Daten wurden nicht korrekt übertragen. Bitte erneut versuchen.", 
                "error",
                )
        else:
            cursor.execute('''
                           UPDATE pets 
                           SET name = %s, description = %s, animal_type_id = %s
                           WHERE pet_id = %s
                           AND owner_id = %s''', 
                           (name, 
                            description, 
                            animal_type_id, 
                            pet_id, 
                            session['current_user']['user_id'],
                            )) 
            connection.commit() 
            connection.close()
            flash(
                "Glückwunsch! Deine Änderungen wurde erfolgreich gespeichert.", 
                "success"
                )
            return redirect(url_for('pet', pet_id=pet_id))
    cursor.execute('''SELECT * 
                FROM pets
                INNER JOIN animal_types 
                ON pets.animal_type_id = animal_types.animal_type_id
                WHERE pets.pet_id = %s
                AND pets.owner_id = %s''', (pet_id, session['current_user']['user_id']))
    pet = cursor.fetchone()
    connection.close()
    if pet is None or animal_types is None:
        abort(404)
    return render_template(
        'edit_pet.html',
        pet=pet,
        animal_types=animal_types, 
        current_user=session['current_user'],
        )


@app.route("/pet/<int:pet_id>/delete")
@login_required
def delete_pet(pet_id):
    """Leer; wird zum Löschen eines Tieres benötigt"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('''SELECT * 
                FROM pets
                WHERE pets.pet_id = %s''', 
                (pet_id,))
    pet = cursor.fetchone()
    if pet is None:
        connection.close()
        flash("Dieses Haustier existiert nicht.", 'error')
        abort(404)
    elif pet['owner_id'] != session['current_user']['user_id']:
        connection.close()
        flash("Du kannst nur deine eigenen Haustiere löschen.", 'error')
        abort(400)
    cursor.execute('''
                   DELETE FROM pets
                   WHERE pet_id = %s
                   AND owner_id = %s
                   ''', (pet_id, session['current_user']['user_id'],))
    connection.commit()
    connection.close()
    flash("Das Haustier wurde erfolgreich gelöscht.", 'success')
    return redirect(url_for('pet_management'))


@app.route("/pet/<int:pet_id>/borrow")
@login_required
def borrow_pet(pet_id):
    """Leer; wird für das Ausleihen benötigt"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('''SELECT * 
                FROM pets
                WHERE pets.pet_id = %s''', 
                (pet_id,))
    pet = cursor.fetchone()
    if pet is None:
        connection.close()
        flash("Dieses Haustier existiert nicht.", 'error')
        abort(404)
    elif pet['owner_id'] == session['current_user']['user_id']:
        connection.close()
        flash("Du kannst deine eigenen Haustiere nicht ausleihen.", 'error')
        abort(400)
    elif not pet['borrower_id'] is None:
        connection.close()
        flash("Dieses Haustier ist bereits verliehen", 'error')
        abort(400)
    cursor.execute('''
                   UPDATE pets 
                   SET borrower_id = %s
                   WHERE pet_id = %s
                   AND borrower_id is NULL''', 
                   (session['current_user']['user_id'],
                    pet_id, 
                    ))
    connection.commit()
    connection.close()
    flash("Du leihst jetzt dieses Haustier aus.", 'success')
    return redirect(url_for('pet', pet_id=pet_id))


@app.route("/pet/<int:pet_id>/return")
@login_required
def return_pet(pet_id):
    """Leer; wird für das Zurückgeben benötigt"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('''SELECT * 
                FROM pets
                WHERE pets.pet_id = %s''', 
                (pet_id,))
    pet = cursor.fetchone()
    if pet is None:
        connection.close()
        flash("Dieses Haustier existiert nicht.", 'error')
        abort(404)
    elif pet['borrower_id'] != session['current_user']['user_id']:
        connection.close()
        flash("Dieses Haustier kann von dir nicht zurückgegeben werden.", 'error')
        abort(400)
    cursor.execute('''
                   UPDATE pets 
                   SET borrower_id = null
                   WHERE pet_id = %s''', 
                   (pet_id,))
    connection.commit()
    connection.close()
    flash("Du hast das Haustier erfolgreich zurückgegeben.", 'success')
    return redirect(url_for('pet', pet_id=pet_id))


@app.route("/pet-management")
@login_required
def pet_management():
    """Verwaltung eigener und geliehener Tiere"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('''SELECT * 
                    FROM pets
                    INNER JOIN animal_types 
                       ON pets.animal_type_id = animal_types.animal_type_id
                   WHERE pets.owner_id = %s''',(session['current_user']['user_id'],)
                   )
    owned_pets = cursor.fetchall()
    cursor.execute('''SELECT * 
                    FROM pets
                    INNER JOIN animal_types 
                       ON pets.animal_type_id = animal_types.animal_type_id
                   INNER JOIN users
                        ON pets.owner_id = users.user_id
                   WHERE pets.borrower_id = %s''',(session['current_user']['user_id'],)
                   )
    borrowed_pets = cursor.fetchall()
    connection.close()
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


@app.route("/pet/new", methods=['GET', 'POST'])
@login_required
def new_pet():
    """Seite zum Anlegen neuer Tiere"""
    filename = None
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('''SELECT * FROM animal_types''')
    animal_types = cursor.fetchall()
    if request.method == 'POST':
        name = request.form.get('Name')
        description = request.form.get('Beschreibung')
        animal_type = request.form.get('Tierart')
        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                filename = str(uuid.uuid4()) + "." + filename.rsplit('.', 1)[1].lower()
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_saved = True
            else:
                flash('Das Bild konnte nicht hochgeladen werden.', 'warning')
        # check if at least one required field is not filled
        if name == "" or description == "" or animal_type == "":
            flash(
                "Einige Daten wurden nicht korrekt übertragen. Bitte erneut versuchen.",
                "error")
        else:
            values= [name, description, animal_type, session['current_user']['user_id']]
            if not filename is None:
                values.append(filename)
            values = tuple(values)
            cursor.execute(f'''
                           INSERT INTO pets 
                           (name, description, animal_type_id, owner_id {', image' if not filename is None else ''}) 
                           VALUES (%s, %s, %s, %s{', %s' if not filename is None else ''})''', values) 
            connection.commit() 
            connection.close()
            flash(
                "Glückwunsch! Dein Haustier wurde erfolgreich gespeichert.", 
                'success'
            )
            return redirect(url_for('pet_management'))
    connection.close()
    return render_template(
        'add_pet.html', 
        animal_types=animal_types, 
        current_user=session['current_user'],
        )


# --- ADMINISTRATION --- #
@app.route("/admin")
@login_required
@admin_required
def admin():
    """Admin-Bereich"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('''SELECT * FROM animal_types''')
    animal_types = cursor.fetchall()
    cursor.execute(f'''SELECT *
                    FROM users
                    INNER JOIN roles 
                       ON users.role_id = roles.role_id
                   ''')
    users = cursor.fetchall()
    connection.close()
    return render_template(
        'admin/admin.html', 
        users=users, 
        current_user=session['current_user'],
        animal_types=animal_types,
        )


@app.route("/admin/user/<int:user_id>/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """Bearbeiten eines Benutzers"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('''SELECT * FROM users
                   WHERE user_id = %s''',
                   (user_id,))
    user = cursor.fetchone()
    cursor.execute('''SELECT * FROM roles''')
    roles = cursor.fetchall()
    if request.method == 'POST':
        role_id = request.form.get('roles')
        # check if at least one required field is not filled
        if role_id == "":
            flash("Erwischt, du Schlauberger!")
        else:
            cursor.execute('''
                   UPDATE users 
                   SET role_id = %s
                   WHERE user_id = %s''', 
                   (role_id, user_id)) 
            connection.commit() 
            connection.close()
            flash(
                "Der Benutzer wurde erfolgreich aktualisiert.", 
                'success'
            )
            return redirect(url_for('admin'))
    connection.close()
    return render_template(
        'admin/edit_user.html', 
        user=user,
        roles= roles,
        current_user=session['current_user'],
        )


@app.route("/admin/user/<int:user_id>/delete", methods=['GET', 'POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Leer; wird zum Löschen eines Benutzers benötigt"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('''
                   DELETE FROM users
                   WHERE user_id = %s
                   ''', (user_id,))
    connection.commit()
    connection.close()
    flash("Der Benutzer wurde erfolgreich gelöscht.", 'success')
    return redirect(url_for('admin'))


@app.route("/admin/animal_type/new", methods=['GET', 'POST'])
@login_required
@admin_required
def new_animal_type():
    """Route für neue Tierarten"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form.get('name')
        # check if at least one required field is not filled
        if name == "":
            flash("Erwischt, du Schlauberger!")
        else:
            cursor.execute('''
                           INSERT INTO animal_types 
                           (animal_type) 
                           VALUES (%s)''', 
                           (name,)) 
            connection.commit() 
            connection.close()
            flash(
                "Glückwunsch! Eine neue Tierart wurde erfolgreich angelegt.", 
                'success'
            )
            return redirect(url_for('admin'))
    connection.close()
    return render_template(
        'admin/new_animal_type.html',
        current_user=session['current_user'],)


@app.route("/admin/animal_type/<int:animal_type_id>/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def edit_animal_type(animal_type_id):
    """Route für die Bearbeitung von Tierarten"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('''SELECT * FROM animal_types
                   WHERE animal_type_id = %s''',
                   (animal_type_id,))
    animal_type = cursor.fetchone()
    if request.method == 'POST':
        name = request.form.get('name')
        # check if at least one required field is not filled
        if name == "":
            flash("Erwischt, du Schlauberger!")
        else:
            cursor.execute('''
                   UPDATE animal_types 
                   SET animal_type = %s
                   WHERE animal_type_id = %s''', 
                   (name, animal_type_id)) 
            connection.commit() 
            connection.close()
            flash(
                "Der Benutzer wurde erfolgreich aktualisiert.", 
                'success'
            )
            return redirect(url_for('admin'))
    connection.close()
    return render_template(
        'admin/edit_animal_type.html',
        animal_type=animal_type,
        current_user=session['current_user'],)


# --- ERRORS --- #
@app.errorhandler(400)
def bad_request(error):
    """Behandelt die 400 Fehler"""
    return render_template('errors/400.html', current_user=session['current_user']), 400


@app.errorhandler(403)
def forbidden(error):
    """Behandelt die 403 Fehler"""
    return render_template('errors/403.html', current_user=session['current_user']), 403


@app.errorhandler(404)
def page_not_found(error):
    """Behandelt die 404 Fehler"""
    return render_template('errors/404.html', current_user=session['current_user']), 404
