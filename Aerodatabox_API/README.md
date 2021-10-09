# AeroDataBox

Die AeroDataBox API wird hier beschrieben: https://www.aerodatabox.com/.

Alle zwei Stunden werden die Abflüge der letzten zwei Stunden abgefragt und in einer DynamoDB Datenbank gespeichert.

[](./Screenshots/AWS_Lambda)

## DynamoBb Datenbank

Als Primary Key wurde das Datum inkl. Uhrzeit gewählt. Als Value werden die abgefragten JSON Elemente als String gespeichert.

[](./Screenshots/AWS_DynamoDB_Store)