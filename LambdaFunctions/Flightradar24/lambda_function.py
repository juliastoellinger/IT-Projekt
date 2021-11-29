import json
import http.client
import boto3
from datetime import datetime
from pyflightdata import FlightData
import dateutil.tz

def lambda_handler(event, context):
    client = boto3.resource("dynamodb")
    table2 = client.Table('flights2')
    table3 = client.Table('flights3')
    table4 = client.Table('flights4')
    
    berlin = dateutil.tz.gettz('Europe/Berlin')
    now = datetime.now(berlin)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    table2.put_item(Item={'date': dt_string, 'data': get_data("FRA")})
    table3.put_item(Item={'date': dt_string, 'data': get_data("VIE")})
    table4.put_item(Item={'date': dt_string, 'data': get_data("AMS")})
    return "done"

def get_data(airport):
    f = FlightData()
    data = f.get_airport_departures(airport, earlier_data=True, limit=10)
    return str(data)