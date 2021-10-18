import boto3
import json

if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('flights')
    data = []

    response = table.scan()
    for item in response['Items']:
        x = item['data']
        y = json.loads(x)
        for dep in y['departures']:
            try:
                data.append(
                    f"{dep['number']}; {dep['departure']['scheduledTimeLocal']}; {dep['departure']['actualTimeLocal']}; {dep['status']}")
            except KeyError:
                pass

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        for item in response['Items']:
            x = item['data']
            y = json.loads(x)
            for dep in y['departures']:
                try:
                    data.append(
                        f"{dep['number']}; {dep['departure']['scheduledTimeLocal']}; {dep['departure']['actualTimeLocal']}; {dep['status']}")
                except KeyError:
                    pass

    outF = open("myOutFile.csv", "w")
    outF.write("number; scheduledTime; actualTime; status")
    for d in data:
        outF.write(d)
        outF.write("\n")
    outF.close()
