import mysql.connector
#from config import Config

TABLES = ["roles", "users", "animal_types", "pets"]
ROLES = [("admin",), ("user",)]
USERS = [
    ("root",1 ),
    ("herbert",2),
    ("herta",2)
]
ANIMAL_TYPES = [("dog",), ("cat",)]
PETS = [
    ("Thor II","Ein nordischer Hund",1,1,None),
    ("Blacky","Eine kleine schwarze Katze",2,1,None),
    ("Mauzi","Eine Katze",1,1,None),
    ("Maggy the Dog","Es ist Maggy!",1,1,None),
    ("Keks","Bitte nicht essen",1,1,None),
    ("Schmackes","Geht ab wie Schmidts Katze",1,2,1,),
    ("Herr von Bödefeld","Hat mehr Klasse als du je haben wirst",2,2,1,)
]


connection = mysql.connector.connect( 
        host="localhost", 
        user="haustierverleih", 
        password="haustierverleih", 
        database="haustierverleih" 
        )

mycursor = connection.cursor()

mycursor.execute("CREATE TABLE roles (role_id INT AUTO_INCREMENT PRIMARY KEY, role VARCHAR(255))")
mycursor.execute("CREATE TABLE users (user_id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password_hash VARCHAR(255), role_id INTEGER, FOREIGN KEY(role_id) REFERENCES roles(role_id))")
mycursor.execute("CREATE TABLE animal_types (animal_type_id INT AUTO_INCREMENT PRIMARY KEY, animal_type VARCHAR(255))")
mycursor.execute("CREATE TABLE pets (pet_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), description VARCHAR(255), animal_type_id INTEGER, FOREIGN KEY(animal_type_id) REFERENCES animal_types(animal_type_id), owner_id INTEGER, FOREIGN KEY(owner_id) REFERENCES users(user_id), borrower_id INTEGER, FOREIGN KEY(borrower_id) REFERENCES users(user_id))")

fill_roles = "INSERT INTO roles (role) VALUES (%s)"
mycursor.executemany(fill_roles, ROLES)
connection.commit()

fill_users = "INSERT INTO users (username, role_id) VALUES (%s, %s)"
mycursor.executemany(fill_users, USERS)
connection.commit()

fill_animal_types = "INSERT INTO animal_types (animal_type) VALUES (%s)"
mycursor.executemany(fill_animal_types, ANIMAL_TYPES)
connection.commit()

fill_pets = "INSERT INTO pets (name, description, animal_type_id, owner_id, borrower_id) VALUES (%s,%s,%s,%s,%s)"
mycursor.executemany(fill_pets, PETS)
connection.commit()