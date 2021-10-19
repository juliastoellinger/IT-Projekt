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

## Extraktion der relevanten Daten und Data Cleaning

Hier sieht die „Architektur“ sehr einfach aus. Die Daten in der DynamoDB Datenbank werden als Json-Objekte abgelegt. Die Daten werden also in ein Python Programm geladen, welches dann mittels Klammernotation auf die relevanten Attribute zugreift und diese in einem csv File speichert.

Wichtiges Detail in der Implementierung ist folgendes: Wenn man die Daten von DynamoDB "scannt" (so wird die Abfrage von mehreren Daten hier bezeichnet), dann wird der Response auf 2mb große Pages aufgeteilt. Man muss deshalb mit einer Schleife über die Pages iterieren, bis kein "LastEveluatedKey" mehr im Response enthalten ist.

`while 'LastEvaluatedKey' in response:`

Ein weiteres Detail: Es können fehlerhafte Daten enthalten sein, die kein scheduledTimeLocal Element enthalten. Diese werden in weiterer Folge einfach ignoriert und nicht weiter verarbeitet: 

                `try:
                    data.append(
                        f"{dep['number']}; {dep['departure']['scheduledTimeLocal']}; {dep['departure']['actualTimeLocal']}; {dep['status']}")
                except KeyError:
                    pass`
