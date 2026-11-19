import mariadb

db_config = {
    "user": "dev",
    "password": "dev",
    "host": "127.0.0.1",
    "database": "haustierverleih",
    "port": 3306,
}

conn = mariadb.connect(**db_config)
cursor = conn.cursor()
