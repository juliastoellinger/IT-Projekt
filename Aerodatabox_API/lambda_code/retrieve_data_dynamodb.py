import boto3

if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('flights')
    response = table.scan()
    print(response)
