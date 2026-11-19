"""USE WITH CAUTION!"""

import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="haustierverleih",
    password="haustierverleih",
    database="haustierverleih",
)

mycursor = connection.cursor()
mycursor.execute("""ALTER TABLE pets ADD image VARCHAR(255)""")
connection.commit()
connection.close()
