# Haustierverleih

Für den Betrieb dieser Webanwendung muss eine .env Datei angelegt werden, die den Benutzernamen und das Passwort für die Datanbank, sowie den Secret Key für Flask enthält.
Beispiel:
```
DATABASE_USER="meindbuser"
DATABASE_PASSWORD="meindbpasswort"
SECRET_KEY="meinsupersichererschlüssel"
```
Secret-Key über diesen Befehl generieren:
```
$ python -c 'import secrets; print(secrets.token_hex())'
```