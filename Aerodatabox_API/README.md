# AeroDataBox

[AeroDataBox API](https://aerodatabox.com) ist eine nützliche Schnittstelle mit verschiedensten Features im Bereich des Flugverkehrs:

* flights
* flight status
* flight delays
* flight schedules
* airports
* airport schedules
* airport delay index
* airport destination statistics
* airport local time
* aircrafts
* aircraft images
* etc...

## Rapid API

Aktuell wird die Schnittstelle ausschließlich über [RapidAPI](https://rapidapi.com/aerodatabox/api/aerodatabox) zur Verfügung gestellt. Man kann die Daten also nur mit einem RapidAPI Account benutzen.

## Spezifika dieser Quelle

Alle zwei Stunden werden die Abflüge der letzten zwei Stunden abgefragt und in einer DynamoDB Datenbank gespeichert.

Die Basic Version dieser Schnittstelle ist auf 200 Endpoints pro Monat limitiert. Deshalb haben wir uns dazu entschieden, dass jeder von uns eine Lambda Funktion erstellt und die Daten von nur einem Flughafen sammelt.

Der Code unterscheidet sich dabei im Wesentlichen nur an folgender Stelle:

`conn.request("GET", f"/flights/airports/icao/EHAM/{from_}/{to_}?withLeg=true&withCancelled=true&withCodeshared=true&withCargo=true&withPrivate=true&withLocation=false", headers=headers)`

Es muss lediglich der Flughafencode angepasst werden: `icao/<Flughafencode>/`
