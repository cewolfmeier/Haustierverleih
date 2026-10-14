from app import app
from markupsafe import escape, Markup

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
        "owner_id": 2,
        "borrower_id": None,
    },
    {
        "pet_id": 3,
        "name": "Mauzi",
        "description": "Eine Katze",
        "animal_type": "cat",
        "owner_id": 3,
        "borrower_id": None,
    },
    {
        "pet_id": 4,
        "name": "Maggy the Dog",
        "description": "Es ist Maggy!",
        "animal_type": "dog",
        "owner_id": 4,
        "borrower_id": None,
    },
    {
        "pet_id": 5,
        "name": "Keks",
        "description": "Bitte nicht essen",
        "animal_type": "dog",
        "owner_id": 5,
        "borrower_id": None,
    },
    {
        "pet_id": 6,
        "name": "Schmackes",
        "description": "Geht ab wie Schmidts Katze",
        "animal_type": "dog",
        "owner_id": 6,
        "borrower_id": 1,
    },
    {
        "pet_id": 7,
        "name": "Herr von Bödefeld",
        "description": "Hat mehr Klasse als du je haben wirst",
        "animal_type": "cat",
        "owner_id": 1,
        "borrower_id": 2,
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
def index():
    """Startseite mit Liste aller Tiere"""
    pets_html = ""
    for pet in pets:
        pets_html += f"""
<li>
    <h2>{escape(pet["name"])}</h2>
    <br>{escape(pet["description"])}
    <br>Besitzer: {pet["owner_id"]}
    <br>{"Aktuell" if pet["borrower_id"] is None else "Nicht"} verfügbar
</li>
"""

    content = f"""
<h1>Haustierverleih</h1>
<p>Registrierte Haustiere</p>
<ul>
{pets_html}
</ul>
"""
    return TEMPLATE_UPPER + content + TEMPLATE_LOWER


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
    content = """"""
    return TEMPLATE_UPPER + content + TEMPLATE_LOWER


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
def pet(pet_id: int):
    """Zeigt die Details eines Tieres an"""
    content = """"""
    return TEMPLATE_UPPER + content + TEMPLATE_LOWER


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
    content = """"""
    return TEMPLATE_UPPER + content + TEMPLATE_LOWER


@app.route("/pet/new")
def new_pet():
    """Seite zum Anlegen neuer Tiere"""
    content = """"""
    return TEMPLATE_UPPER + content + TEMPLATE_LOWER


@app.errorhandler(404)
def page_not_found(error):
    """Behandelt die 404 Fehler"""
    content = """
<h1>404 - Haustier nicht gefunden</h1>
<p>Ups, da ist uns wohl ein Haustier entfleucht. Wir fangen es schnell wieder ein.</p>
"""
    return TEMPLATE_UPPER + content + TEMPLATE_LOWER
