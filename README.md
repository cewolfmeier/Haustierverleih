# Haustierverleih

> Hinweis: Dies ist keine Anwendung, die produktiv läuft. Dieses Repo dient mir als Spielwiese zum lernen und ausprobieren. Vielleicht ist was Interessantes dabei.

Für den Betrieb dieser Webanwendung muss eine .env Datei angelegt werden. Siehe .env.example

Secret-Key für die .env über diesen Befehl generieren:
```
$ python -c 'import secrets; print(secrets.token_hex())'
```