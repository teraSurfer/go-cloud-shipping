import json
from util.constants import *
from util import utilities
import decimal


dynamodb = None

def handler(event, context):
    global dynamodb
    if not dynamodb:
        dynamodb = utilities.get_dynamodb_client(event)

    #print(event)
    request = json.loads(event['body'])

    table = dynamodb.Table(PRICES_TABLE)
    source = request[SOURCE_DIVISION_KEY]
    destination = request[DESTINATION_DIVISION_KEY]
    price = request['price']
    vendor_email = request['v_email']

    table = dynamodb.Table(PRICES_TABLE)
    response = table.get_item(
        Key={
            SOURCE_DIVISION_COLUMN: request[SOURCE_DIVISION_KEY]
        }
    )

    print(response)
    oldprice = response['Item'][destination]['Price']

    if int(oldprice) > int(price):
        response = table.update_item(
            Key={
                SOURCE_DIVISION_COLUMN: source
            },
            UpdateExpression="set " + destination + " = :p",
            ExpressionAttributeValues={
                ':p': {PRICE_COLUMN: decimal.Decimal(price), V_EMAIL_COLUMN: vendor_email}
            },

            ReturnValues="UPDATED_NEW"
        )

        return {'statusCode': 200,
                'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": "*"}}
    else:
        return {'statusCode': 201,
                'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": "*"}}