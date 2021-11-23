import boto3
import json
import time

if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('flights2')
    data = []
    data.append(f"number;scheduledTime;actualTime")
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
                #print(flight)
                #if real and estimated departure time is 'None' we have no basis on which we could caluclate a difference to the scheduled departure time --> sort out
                try:
                    flight['flight']['identification']['number']['default']
                    flight['flight']['time']['scheduled']['departure_date']
                    flight['flight']['time']['scheduled']['departure_time']
                except KeyError:
                    pass
                if (flight['flight']['time']['real']['departure'] == 'None' and flight['flight']['airline']=='None' and flight['flight']['time']['estimated']['departure'] == 'None') or flight['flight']['time']['scheduled']['departure_date'] == 'None':
                    pass
                else:
                    try:
                        scheduledTimeUTC = time.mktime(time.strptime(flight['flight']['time']['scheduled']['departure_date']+flight['flight']['time']['scheduled']['departure_time'], "%Y%m%d%H%M"))
                        actualTimeUTC = time.mktime(time.strptime(flight['flight']['time']['scheduled']['departure_date']+flight['flight']['time']['estimated']['departure_time'], "%Y%m%d%H%M"))
                        airline = ""
                        if (flight['flight']['airline']=='None'):
                            airline = 'None'
                        else:
                            airline = flight['flight']['airline']['name']
                        data.append(f"{airline}+{flight['flight']['identification']['number']['default']};{scheduledTimeUTC};{actualTimeUTC}")

                    except KeyError:
                        try:
                            data.append(f"{airline}+{flight['flight']['identification']['number']['default']};{scheduledTimeUTC};{actualTimeUTC}")
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
                                scheduledTimeUTC = time.mktime(time.strptime(
                                    flight['flight']['time']['scheduled']['departure_date'] +
                                    flight['flight']['time']['scheduled']['departure_time'], "%Y%m%d%H%M"))
                                actualTimeUTC = time.mktime(time.strptime(
                                    flight['flight']['time']['scheduled']['departure_date'] +
                                    flight['flight']['time']['estimated']['departure_time'], "%Y%m%d%H%M"))
                                airline = ""
                                if (flight['flight']['airline'] == 'None'):
                                    airline = 'None'
                                else:
                                    airline = flight['flight']['airline']['name']
                                data.append(f"{airline}+{flight['flight']['identification']['number']['default']};{scheduledTimeUTC};{actualTimeUTC}")
                            except KeyError:
                                try:
                                    data.append(
                                        f"{airline}+{flight['flight']['identification']['number']['default']};{scheduledTimeUTC};{actualTimeUTC}")
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
