# IT-Projekt

## Aufgabe 1

### Aufgabenbeschreibung

Datenquellen identifizieren
Daten sammeln und herunterladen
Relevante Attribute extrahieren
Daten validieren (Cleaning)

#### Datequellen identifizieren

* [Flightradar24](./Flightradar24)
* [AeroDataBox](./Aerodatabox_API)

#### Daten sammeln

##### AWS

Als Infrastruktur für die Datensammlung wählten wir AWS, den Cloud Service von Amazon aus. Der Code für die Datensammlung wird in AWS Lambda Funktionen ausgeführt und die Daten werden in AWS DynamoDB gespeichert. Gründe für die Wahl des Amazon Cloud Services sind folgende:
* Komfortable periodische Ausführung der Lambda Funktionen mittels EventBridge cronjobs
* Kein lokales Speichern der großen Datenmengen
* Dynamische Erweiterung des Speicherplatz
* Es wird kein zusätzlicher Rechner benötigt, der eine Woche mit der Datensammlung beschäftigt wäre
* Zuverlässigkeit der AWS Services

Wichtige Ressourcen: 

* [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/index.html)
* [AWS DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/index.html)
* [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

##### Flughäfen

FRA, VIE, EHAM


#### Relevante Attribute extrahieren

#### Datencleaning

## Aufgabe 2
