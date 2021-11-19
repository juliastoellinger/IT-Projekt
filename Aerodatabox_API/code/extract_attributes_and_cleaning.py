import boto3
import json
import time

if __name__ == '__main__':
    # Connection to dynamodb database
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('flights')
    data = []

    # get all elements from table - problem: boto3 splits the result in pages of 2 mb
    response = table.scan()
    for item in response['Items']:
        x = item['data']
        y = json.loads(x)
        try:
            for dep in y['departures']:
                # try catch because there might be elements with no scheduledTimeLocal- element. We need to filter them out.
                try:
                    scheduledTimeUTC = time.mktime(time.strptime(dep['departure']['scheduledTimeUtc'], "%Y-%m-%d %H:%MZ"))
                    actualTimeUTC = time.mktime(time.strptime(dep['departure']['actualTimeUtc'], "%Y-%m-%d %H:%MZ"))
                    data.append(
                        f"{dep['airline']['name']}+{dep['number']};{scheduledTimeUTC};{actualTimeUTC};{dep['status']}")
                except KeyError:
                    pass
        except KeyError:
            pass

    # because of the "pagination" we need to iterate over the pages as long as there is no page left
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        for item in response['Items']:
            x = item['data']
            y = json.loads(x)
            try:
                for dep in y['departures']:
                    # try catch because there might be elements with no scheduledTimeLocal- element. We need to filter them out.
                    try:
                        scheduledTimeUTC = time.mktime(
                            time.strptime(dep['departure']['scheduledTimeUtc'], "%Y-%m-%d %H:%MZ"))
                        actualTimeUTC = time.mktime(time.strptime(dep['departure']['actualTimeUtc'], "%Y-%m-%d %H:%MZ"))
                        data.append(
                            f"{dep['airline']['name']}+{dep['number']};{scheduledTimeUTC};{actualTimeUTC};{dep['status']}")
                    except KeyError:
                        pass
            except KeyError:
                pass

    # write all the elements to a .csv file
    outF = open("aerodata_flughafen_amsterdam.csv", "w")
    outF.write("number;scheduledTime;actualTime;status")
    outF.write("\n")
    for d in data:
        outF.write(d)
        outF.write("\n")
    outF.close()
