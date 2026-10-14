# Haustierverleih

> Hinweis: Dies ist keine Anwendung, die produktiv läuft. Dieses Repo dient mir als Spielwiese zum lernen und ausprobieren. Vielleicht ist was Interessantes dabei.

## Was ist ein Haustierverleih?
Der "Haustierverleih" enstand als eine Art Kleinanzeigen-Web-Projekt meiner Ausbildung zum Informatiker f. Anwendungsentwicklung.

Es vermittelt die Grundlagen der Web-Entwicklung mithilfe des Python-Frameworks Flask.

Für den Betrieb dieser Webanwendung muss eine .env Datei angelegt werden. Siehe .env.example

Secret-Key für die .env über diesen Befehl generieren:
```
$ python -c 'import secrets; print(secrets.token_hex())'
```