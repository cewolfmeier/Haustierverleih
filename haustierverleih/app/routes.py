from app import app
from flask import url_for, render_template
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
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.execute('SELECT * FROM roles')
    roles = cursor.fetchall()
    connection.close()
    for user in users:
        for role in roles:
            if user["role_id"] == role["role_id"]:
                user["role"] = role["role"]
    return render_template('admin.html', users=users, current_user=current_user)


@app.route("/edit_user")
def edit_user():
    """Bearbeiten eines Benutzers"""
    return render_template('edit_user.html')


@app.route("/delete_user")
def delete_user():
    """Leer; wird zum Löschen eines Benutzers benötigt"""
    pass


@app.route("/pet/<pet_id>")
def pet(pet_id):
    """Zeigt die Details eines Tieres an"""
    pet = None
    if pet_id.isdecimal():
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


@app.route("/pet/<pet_id>/edit")
def edit_pet(pet_id: int):
    """Seite zum Bearbeiten eines Tieres"""
    pet = None
    if pet_id.isdecimal():
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f'''SELECT * 
                    FROM pets
                    INNER JOIN animal_types 
                       ON pets.animal_type_id = animal_types.animal_type_id
                    WHERE pets.pet_id = {pet_id}''')
        pet = cursor.fetchone()
    return render_template('edit_pet.html', pet=pet, current_user=current_user)


@app.route("/pet/<pet_id>/delete")
def delete_pet(pet_id: int):
    """Leer; wird zum Löschen eines Tieres benötigt"""
    pass


@app.route("/pet/<pet_id>/borrow")
def borrow_pet(pet_id: int):
    """Leer; wird für das Ausleihen benötigt"""
    pass


@app.route("/pet/<pet_id>/return")
def return_pet(pet_id: int):
    """Leer; wird für das Zurückgeben benötigt"""
    pass


@app.route("/pet-management")
def pet_management():
    """Verwaltung eigener und geliehener Tiere"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f'''SELECT * 
                    FROM pets
                    INNER JOIN animal_types 
                       ON pets.animal_type_id = animal_types.animal_type_id
                   ''')
    pets = cursor.fetchall()
    connection.close()
    owned_pets = []
    owned_pets_counter = 0
    borrowed_pets = []
    borrowed_pets_counter = 0
    for pet in pets:
        if pet["owner_id"] == current_user["user_id"]:
            owned_pets.append(pet)
            owned_pets_counter += 1
        elif pet["borrower_id"] == current_user["user_id"]:
            borrowed_pets.append(pet)
            borrowed_pets_counter += 1
    return render_template(
        'pet_management.html', 
        borrowed_pets=borrowed_pets, 
        owned_pets=owned_pets, 
        owned_pets_counter=owned_pets_counter, 
        borrowed_pets_counter=borrowed_pets_counter, 
        current_user=current_user,
        )


@app.route("/pet/new")
def new_pet():
    """Seite zum Anlegen neuer Tiere"""
    return render_template('add_pet.html')


@app.errorhandler(404)
def page_not_found(error):
    """Behandelt die 404 Fehler"""
    return render_template('errors/404.html', current_user=current_user), 404
