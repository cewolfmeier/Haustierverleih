from app import app
from flask import url_for, render_template
from markupsafe import escape, Markup

current_user = {
    "user_id": 1,
    "username": "root"
}
ROLES = [
    {
        "role_id": 1,
        "role": 'admin'
    },
    {
        "role_id": 2,
        "role": 'user'
    },
]
USERS = [
    {
        "user_id": 1,
        "username": "root",
        "role_id": 1
    },
    {
        "user_id": 2,
        "username": "herbert",
        "role_id": 2
    },
    {
        "user_id": 3,
        "username": "herta",
        "role_id": 2
    }
]
pets = [
    {
        "pet_id": 1,
        "name": "Thor II",
        "description": "Ein nordischer Hund",
        "animal_type": "dog",
        "owner_id": 1,
        "borrower_id": None,
    },
    {
        "pet_id": 2,
        "name": "Blacky",
        "description": "Eine kleine schwarze Katze",
        "animal_type": "cat",
        "owner_id": 1,
        "borrower_id": None,
    },
    {
        "pet_id": 3,
        "name": "Mauzi",
        "description": "Eine Katze",
        "animal_type": "cat",
        "owner_id": 1,
        "borrower_id": None,
    },
    {
        "pet_id": 4,
        "name": "Maggy the Dog",
        "description": "Es ist Maggy!",
        "animal_type": "dog",
        "owner_id": 1,
        "borrower_id": None,
    },
    {
        "pet_id": 5,
        "name": "Keks",
        "description": "Bitte nicht essen",
        "animal_type": "dog",
        "owner_id": 1,
        "borrower_id": None,
    },
    {
        "pet_id": 6,
        "name": "Schmackes",
        "description": "Geht ab wie Schmidts Katze",
        "animal_type": "dog",
        "owner_id": 2,
        "borrower_id": 1,
    },
    {
        "pet_id": 7,
        "name": "Herr von Bödefeld",
        "description": "Hat mehr Klasse als du je haben wirst",
        "animal_type": "cat",
        "owner_id": 2,
        "borrower_id": 1,
    },
]

TEMPLATE_UPPER = """
<!doctype html>
<html lang="de">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1"> 
        <title>Haustierverleih</title> 
    </head> 
    <body>
"""

TEMPLATE_LOWER = """
    </body> 
</html>
"""

@app.route("/")
@app.route("/index")
def index():
    """Startseite mit Liste aller Tiere"""
    return render_template('index.html', pets=pets, current_user=current_user)


@app.route("/login")
def login():
    """Login-Seite"""
    content = """"""
    return TEMPLATE_UPPER + content + TEMPLATE_LOWER


@app.route("/register")
def register():
    """Seite zur Account-Erstellung"""
    content = """"""
    return TEMPLATE_UPPER + content + TEMPLATE_LOWER


@app.route("/logout")
def logout():
    """Leer; wird für den Logout benötigt"""
    pass


@app.route("/admin")
def admin():
    """Admin-Bereich"""
    users = USERS
    for user in users:
        for role in ROLES:
            if user["role_id"] == role["role_id"]:
                user["role"] = role["role"]
    return render_template('admin.html', users=users, current_user=current_user)


@app.route("/edit_user")
def edit_user():
    """Bearbeiten eines Benutzers"""
    content = """"""
    return TEMPLATE_UPPER + content + TEMPLATE_LOWER


@app.route("/delete_user")
def delete_user():
    """Leer; wird zum Löschen eines Benutzers benötigt"""
    pass


@app.route("/pet/<pet_id>")
def pet(pet_id):
    """Zeigt die Details eines Tieres an"""
    pet_dict = None   
    if pet_id.isdecimal(): 
        pet_id = int(pet_id)
        for pet in pets:
            if pet["pet_id"] == pet_id:
                pet_dict = pet
                break
    return render_template('pet.html', pet=pet_dict, current_user=current_user)


@app.route("/pet/<pet_id>/edit")
def edit_pet(pet_id: int):
    """Seite zum Bearbeiten eines Tieres"""
    content = """"""
    return TEMPLATE_UPPER + content + TEMPLATE_LOWER


@app.route("/pet/<pet_id>/delete")
def delete_pet(pet_id: int):
    """Leer; wird zum Löschen eines Tieres benötigt"""
    pass


@app.route("/pet/<pet_id>/borrow")
def borrow_pet(pet_id: int):
    """Leer; wird für das Ausleihen benötigt"""
    content = """"""
    return TEMPLATE_UPPER + content + TEMPLATE_LOWER


@app.route("/pet/<pet_id>/return")
def return_pet(pet_id: int):
    """Leer; wird für das Zurückgeben benötigt"""
    content = """"""
    return TEMPLATE_UPPER + content + TEMPLATE_LOWER


@app.route("/pet-management")
def pet_management():
    """Verwaltung eigener und geliehener Tiere"""
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
        'pet-management.html', 
        borrowed_pets=borrowed_pets, 
        owned_pets=owned_pets, 
        owned_pets_counter=owned_pets_counter, 
        borrowed_pets_counter=borrowed_pets_counter, 
        current_user=current_user,
        )


@app.route("/pet/new")
def new_pet():
    """Seite zum Anlegen neuer Tiere"""
    content = """"""
    return TEMPLATE_UPPER + content + TEMPLATE_LOWER


@app.errorhandler(404)
def page_not_found(error):
    """Behandelt die 404 Fehler"""
    content = f"""
    <a href="{url_for("index")}">zurück zur Startseite</a>
    <h1>404 - Haustier nicht gefunden</h1>
    <p>Ups, da ist uns wohl ein Haustier entfleucht. Wir fangen es schnell wieder ein.</p>
"""
    return TEMPLATE_UPPER + content + TEMPLATE_LOWER
