'''USE WITH CAUTION!'''
import mysql.connector
from werkzeug.security import generate_password_hash

TABLES = ["roles", "users", "animal_types", "pets"]
ROLES = [("admin",), ("user",)]
USERS = [
    ("root",1 ),
    ("herbert",2),
    ("herta",2)
]
connection = mysql.connector.connect( 
        host="localhost", 
        user="", 
        password="", 
        database="haustierverleih" 
        )

mycursor = connection.cursor()
mycursor.execute('''UPDATE users SET password_hash = %s WHERE username = %s''', (generate_password_hash('root'), 'root'))
mycursor.execute('''UPDATE users SET password_hash = %s WHERE username = %s''', (generate_password_hash('herbert'), 'herbert'))
mycursor.execute('''UPDATE users SET password_hash = %s WHERE username = %s''', (generate_password_hash('herta'), 'herta'))
connection.commit()
connection.close()