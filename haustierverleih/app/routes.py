from app import app
from flask import render_template

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


@app.route("/")
def index():
    """Startseite mit Liste aller Tiere"""
    pass


@app.route("/login")
def login():
    """Login-Seite"""
    pass


@app.route("/register")
def index():
    """Seite zur Account-Erstellung"""
    pass


@app.route("/logout")
def index():
    """Leer; wird für den Logout benötigt"""
    pass


@app.route("/admin")
def index():
    """Admin-Bereich"""
    pass


@app.route("/edit_user")
def index():
    """Bearbeiten eines Benutzers"""
    pass


@app.route("/delete_user")
def index():
    """Leer; wird zum Löschen eines Benutzers benötigt"""
    pass


@app.route("/pet/<pet_id>")
def index(pet_id: int):
    """Zeigt die Details eines Tieres an"""
    pass


@app.route("/pet/<pet_id>/edit")
def index(pet_id: int):
    """Seite zum Bearbeiten eines Tieres"""
    pass


@app.route("/pet/<pet_id>/delete")
def index(pet_id: int):
    """Leer; wird zum Löschen eines Tieres benötigt"""
    pass


@app.route("/pet/<pet_id>/borrow")
def index(pet_id: int):
    """Leer; wird für das Ausleihen benötigt"""
    pass


@app.route("/pet/<pet_id>/return")
def index(pet_id: int):
    """Leer; wird für das Zurückgeben benötigt"""
    pass


@app.route("/pet-management")
def index():
    """Verwaltung eigener und geliehener Tiere"""
    pass


@app.route("/pet/new")
def index():
    """Seite zum Anlegen neuer Tiere"""
    pass


@app.errorhandler(404)
def page_not_found():
    """Behandelt die 404 Fehler"""