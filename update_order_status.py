import json
from util.constants import *
from util import utilities
import decimal


dynamodb = None

def handler(event, context):
    global dynamodb
    if not dynamodb:
        dynamodb = utilities.get_dynamodb_client(event)

    request = json.loads(event['body'])

    table = dynamodb.Table(ORDERS_TABLE)
    orderid = request[ORDER_ID_KEY]
    orderstatus = request[ORDER_STATUS_KEY]

    response = table.update_item(
        Key={
            ID_COLUMN: orderid
        },
        UpdateExpression="set " + STATUS_COLUMN + " = :s",
        ExpressionAttributeValues={
            ':s': orderstatus
        },

        ReturnValues="UPDATED_NEW"
    )

    return {'statusCode': 200,
            'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": "*"}}
