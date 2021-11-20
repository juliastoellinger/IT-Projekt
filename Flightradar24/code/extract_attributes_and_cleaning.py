import boto3
import json

if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('flights2')
    data = []
    data.append(f"number;date;scheduled_departure_time;real_departure;estimated_departure")
    json_decode_error_counter = 0

    response = table.scan()
    for item in response['Items']:
        string = item['data']
        string = string.replace("\'", "\"")
        string = string.replace("True", "\"True\"")
        string = string.replace("False", "\"False\"")
        try:
            flights = json.loads(string)
            for flight in flights:
                #if real and estimated departure time is 'None' we have no basis on which we could caluclate a difference to the scheduled departure time --> sort out
                try:
                    flight['flight']['identification']['number']['default']
                    flight['flight']['time']['scheduled']['departure_date']
                    flight['flight']['time']['scheduled']['departure_time']
                except KeyError:
                    pass
                if (flight['flight']['time']['real']['departure'] == 'None' and flight['flight']['time']['estimated']['departure'] == 'None') or flight['flight']['time']['scheduled']['departure_date'] == 'None':
                    pass
                else:
                    try:
                        data.append(f"{flight['flight']['identification']['number']['default']};{flight['flight']['time']['scheduled']['departure_date']};{flight['flight']['time']['scheduled']['departure_time']};{flight['flight']['time']['real']['departure']};{flight['flight']['time']['estimated']['departure_time']}")
                    except KeyError:
                        try:
                            data.append(f"{flight['flight']['identification']['number']['default']};{flight['flight']['time']['scheduled']['departure_date']};{flight['flight']['time']['scheduled']['departure_time']};{flight['flight']['time']['real']['departure_time']};None")
                        except KeyError:
                            pass
        except json.decoder.JSONDecodeError:
            json_decode_error_counter = json_decode_error_counter+1
            pass

    # because of the "pagination" we need to iterate over the pages as long as there is no page left
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        for item in response['Items']:
            string = item['data']
            string = string.replace("\'", "\"")
            string = string.replace("True", "\"True\"")
            string = string.replace("False", "\"False\"")
            try:
                flights = json.loads(string)
                for flight in flights:
                    # if real and estimated departure time is 'None' we have no basis on which we could caluclate a difference to the scheduled departure time --> sort out
                    try:
                        flight['flight']['identification']['number']['default']
                        flight['flight']['time']['scheduled']['departure_date']
                        flight['flight']['time']['scheduled']['departure_time']
                    except KeyError:
                        pass
                    if (flight['flight']['time']['real']['departure'] == 'None' and
                        flight['flight']['time']['estimated']['departure'] == 'None') or \
                            flight['flight']['time']['scheduled']['departure_date'] == 'None':
                        pass
                    else:
                        try:
                            data.append(
                                f"{flight['flight']['identification']['number']['default']};{flight['flight']['time']['scheduled']['departure_date']};{flight['flight']['time']['scheduled']['departure_time']};{flight['flight']['time']['real']['departure']};{flight['flight']['time']['estimated']['departure_time']}")
                        except KeyError:
                            try:
                                data.append(
                                    f"{flight['flight']['identification']['number']['default']};{flight['flight']['time']['scheduled']['departure_date']};{flight['flight']['time']['scheduled']['departure_time']};{flight['flight']['time']['real']['departure_time']};None")
                            except KeyError:
                                pass
            except json.decoder.JSONDecodeError:
                json_decode_error_counter = json_decode_error_counter + 1
                pass

    outF = open("myOutFile.csv", "w")
    outF.write("\n")
    for d in data:
        outF.write(d)
        outF.write("\n")
    outF.close()

    print(f"Json Decode Error Counter: {json_decode_error_counter}")
