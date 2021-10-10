# Flightradar24

[Flightradar24.com](https://www.flightradar24.com/) ist ein Onlinedienst zur Echtzeit-Positionsdarstellung von Flugzeugen. Er wird von dem in Stockholm ansässigen Unternehmen Flightradar24 AB betrieben.

## pyflightdata API

* [API Dokumentation](https://pyflightdata.readthedocs.io/en/latest/pyflightdata.html)

* Lambda Layer (dependencies): `./code/python.zip`

### Relevante Methoden

Abflüge auf einem bestimmten Flughafen: `get_airport_departures(iata, page=1, limit=100, earlier_data=False)`

Wetter auf dem Flughafen: `get_airport_weather(iata, page=1, limit=100)`

Flughistorie für einen bestimmten Flug: `get_all_available_history_by_flight_number(flight_number, delay=1)`

## Spezifika dieser Quelle

Ein Problem dieser Schnittstelle ist folgendes: Man kann hier leider kein Zeitintervall auswählen, für das man die Flüge abfragen möchte. Deshalb erfolgte eine Schätzung (auf Basis der veröffentlichten [Daten und Fakten](https://www.fraport.com/de/konzern/ueber-uns/zahlen--daten-und-fakten1.html) des Frankfurter Flughafens), wie viele Flugzeuge pro Stunde abheben. Es finden ungefähr 1400 Flüge in 24 Stunden statt. Das entspricht wahrscheinlich 700 Abflüge in 24 Stunden und 30 Abflüge pro Stunde. Dabei muss man beachten, dass der Großteil der Flüge zwischen 9:00 und 21:00 stattfinden (siehe Flightradar). Es wird also ein Abfrage-Intervall von 10 Minuten im Zeitraum 9:00 bis 21:00 festgelegt, in dem jeweils 10 Flüge abgefragt werden. Überflüssige Flüge müssen dann im Nachhinein bereinigt werden.

## Ansatz

1) Abfüge von einem bestimmten Flughafen abfragen. (Achtung: Spezifika dieser Quelle beachten)
2) Flughistorie eines Flugs abfragen. Nur sinnvoll, wenn kostenpflichtig die Daten für ein Jahr abgefragt werden.
