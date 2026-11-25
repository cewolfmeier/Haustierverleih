# Haustierverleih

> Hinweis: Dies ist keine Anwendung, die produktiv läuft. Dieses Repo dient mir als Spielwiese zum Lernen und Ausprobieren.

## Was ist ein Haustierverleih?
Der "Haustierverleih" enstand als eine Art Kleinanzeigen-Web-Projekt meiner Ausbildung zum Informatiker f. Anwendungsentwicklung.

Es vermittelt die Grundlagen der Web-Entwicklung mithilfe des Python-Frameworks Flask.

## Installation und Einrichtung der Dev-Umgebung

Eventuell muss der MariaDB-Connector für das jeweilige Betriebssystem nachgeladen werden.

Für den Betrieb dieser Webanwendung muss eine .env Datei angelegt werden. Siehe .env.example

Secret-Key für die .env über diesen Befehl generieren:
```
$ python -c 'import secrets; print(secrets.token_hex())'
```

Für den ersten Start (sobald die DB läuft):
- im src Ordner: `flask db upgrade` (Tabellen initialisieren)
- setup.py starten
- wenn fertig und erfolgreich: `flask run` zum starten als dev-server

## Warum sieht die Commit-Historie so seltsam aus?
Das Repo lag bis vor Oktober 2026 auf dem Gitlab-Server der Ausbildungseinrichtung. Mangels besserem Können wurde beim Umstellen der Email Adresse auch die Historie neu geschrieben. 
Das Ursprungsprojekt entstand im Oktober/November 2025.
