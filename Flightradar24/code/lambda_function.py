import json
import http.client
import boto3
from datetime import datetime
from pyflightdata import FlightData
import dateutil.tz

def lambda_handler(event, context):
    client = boto3.resource("dynamodb")
    table = client.Table('flights2')
    
    berlin = dateutil.tz.gettz('Europe/Berlin')
    now = datetime.now(berlin)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data = get_data()
    data = str(data)
    response = table.put_item(Item={'date': dt_string, 'data': data})
    return response

def get_data():
    f = FlightData()
    data = f.get_airport_departures("FRA", earlier_data=True, limit=10)
    return data
