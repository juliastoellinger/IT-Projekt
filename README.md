# IT-Projekt

## Aufgabe 1

### Aufgabenbeschreibung

#### Daten sammeln

Als Infrastruktur für die Datensammlung wählten wir AWS, den Cloud Service von Amazon aus. Der Code für die Datensammlung wird in AWS Lambda Funktionen ausgeführt und die Daten werden in AWS DynamoDb gespeichert. Gründe für die Wahl des Amazon Cloud Services sind folgende:
* Komfortable periodische Ausführung der Lambda Funktionen mittels EventBridge cronjobs
* Kein lokales Speichern der großen Datenmengen
* Dynamische Erweiterung des Speicherplatz
* Es wird kein zusätzlicher Rechner benötigt, der eine Woche mit der Datensammlung beschäftigt wäre
* Zuverlässigkeit der AWS Services
