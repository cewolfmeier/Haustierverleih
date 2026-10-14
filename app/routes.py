from app import app
from flask import render_template, redirect, request, url_for, flash
import mysql.connector
from config import Config

def get_db_connection(): 
    connection = mysql.connector.connect( 
        host="localhost", 
        user=Config.DATABASE_USER, 
        password=Config.DATABASE_PASSWORD, 
        database="haustierverleih" 
        ) 
    return connection

current_user = {
    "user_id": 1,
    "username": "root"
}

@app.route("/")
@app.route("/index")
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
    return render_template('index.html', pets=pets, current_user=current_user)


@app.route("/login")
def login():
    """Login-Seite"""
    return render_template('auth/login.html')


@app.route("/register")
def register():
    """Seite zur Account-Erstellung"""
    return render_template('auth/register.html')


@app.route("/logout")
def logout():
    """Leer; wird für den Logout benötigt"""
    pass


@app.route("/admin")
def admin():
    """Admin-Bereich"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f'''SELECT *
                    FROM users
                    INNER JOIN roles 
                       ON users.role_id = roles.role_id
                   ''')
    users = cursor.fetchall()
    connection.close()
    return render_template('admin.html', users=users, current_user=current_user)


@app.route("/edit_user")
def edit_user():
    """Bearbeiten eines Benutzers"""
    return render_template('edit_user.html')


@app.route("/delete_user")
def delete_user():
    """Leer; wird zum Löschen eines Benutzers benötigt"""
    pass


@app.route("/pet/<int:pet_id>")
def pet(pet_id):
    """Zeigt die Details eines Tieres an"""
    pet = None
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f'''SELECT * 
                FROM pets
                INNER JOIN animal_types 
                    ON pets.animal_type_id = animal_types.animal_type_id
                WHERE pets.pet_id = {pet_id}''')
    pet = cursor.fetchone()
    connection.close()
    return render_template('pet.html', pet=pet, current_user=current_user)


@app.route("/pet/<int:pet_id>/edit", methods=['GET', 'POST'])
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
            flash("Erwischt, du Schlauberger!")
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
                            current_user['user_id'],
                            )) 
            connection.commit() 
            connection.close()
            flash("Glückwunsch! Deine Änderungen wurde erfolgreich gespeichert.")
            return redirect(url_for('pet', pet_id=pet_id))
    else:
        pet = None
        cursor.execute('''SELECT * 
                    FROM pets
                    INNER JOIN animal_types 
                    ON pets.animal_type_id = animal_types.animal_type_id
                    WHERE pets.pet_id = %s
                    AND pets.owner_id = %s''', (pet_id, current_user['user_id']))
        pet = cursor.fetchone()
    connection.close()
    return render_template(
        'edit_pet.html',
        pet=pet,
        animal_types=animal_types, 
        current_user=current_user,
        )


@app.route("/pet/<int:pet_id>/delete")
def delete_pet(pet_id):
    """Leer; wird zum Löschen eines Tieres benötigt"""
    pass


@app.route("/pet/<int:pet_id>/borrow")
def borrow_pet(pet_id):
    """Leer; wird für das Ausleihen benötigt"""
    pass


@app.route("/pet/<int:pet_id>/return")
def return_pet(pet_id):
    """Leer; wird für das Zurückgeben benötigt"""
    pass


@app.route("/pet-management")
def pet_management():
    """Verwaltung eigener und geliehener Tiere"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('''SELECT * 
                    FROM pets
                    INNER JOIN animal_types 
                       ON pets.animal_type_id = animal_types.animal_type_id
                   WHERE pets.owner_id = %s''',(current_user['user_id'],)
                   )
    owned_pets = cursor.fetchall()
    cursor.execute('''SELECT * 
                    FROM pets
                    INNER JOIN animal_types 
                       ON pets.animal_type_id = animal_types.animal_type_id
                   WHERE pets.borrower_id = %s''',(current_user['user_id'],)
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
        current_user=current_user,
        )


@app.route("/pet/new", methods=['GET', 'POST'])
def new_pet():
    """Seite zum Anlegen neuer Tiere"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('''SELECT * FROM animal_types''')
    animal_types = cursor.fetchall()
    if request.method == 'POST':
        name = request.form.get('Name')
        description = request.form.get('Beschreibung')
        animal_type = request.form.get('Tierart')
        # check if at least one required field is not filled
        if name == "" or description == "":
            flash("Erwischt, du Schlauberger!")
        else:
            cursor.execute('INSERT INTO pets (name, description, animal_type_id, owner_id) VALUES (%s, %s, %s, %s)', 
                           (name, description, animal_type, current_user['user_id'])) 
            connection.commit() 
            connection.close()
            flash("Glückwunsch! Dein Haustier wurde erfolgreich gespeichert.")
            return redirect(url_for('pet_management'))
    connection.close()
    return render_template('add_pet.html', animal_types=animal_types, current_user=current_user)


@app.errorhandler(404)
def page_not_found(error):
    """Behandelt die 404 Fehler"""
    return render_template('errors/404.html', current_user=current_user), 404
