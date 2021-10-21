import json
import http.client
import boto3
from datetime import datetime, timedelta
import dateutil.tz

def lambda_handler(event, context):
    client = boto3.resource("dynamodb")
    table = client.Table('flights')
    berlin = dateutil.tz.gettz('Europe/Berlin')
    now = datetime.now(berlin)
    data = get_data(now)
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    response = table.put_item(Item={'date': dt_string, 'data': data})
    return response

    
def get_data(now):
    conn = http.client.HTTPSConnection("aerodatabox.p.rapidapi.com")

    headers = {
        'x-rapidapi-host': "aerodatabox.p.rapidapi.com",
        'x-rapidapi-key': "INSERT RAPID API KEY HERE"
    }
    
    d = now - timedelta(hours=2, minutes=00)
    from_ = d.strftime("%Y-%m-%dT%H:%M")
    to_ = now.strftime("%Y-%m-%dT%H:%M")
    conn.request("GET", f"/flights/airports/icao/EHAM/{from_}/{to_}?withLeg=true&withCancelled=true&withCodeshared=true&withCargo=true&withPrivate=true&withLocation=false", headers=headers)
    res = conn.getresponse()
    data = res.read().decode('utf8')
    return data

