import boto3
import json
from util.constants import *
from util import utilities
import os
from boto3.dynamodb.conditions import Key, Attr

dynamodb = None

def handler(event, context):
    global dynamodb
    if not dynamodb:
        dynamodb = utilities.get_dynamodb_client(event)


    table = dynamodb.Table(ORDERS_TABLE)

    response = table.scan(
        FilterExpression= Key(U_EMAIL_COLUMN).eq(event[PARAMS]['u_email']) & Key(ID_COLUMN).eq(int(event[PARAMS]['id']))
    )
    print(response)
    data =response['Items'][0]

    data = {k.lower(): v for k, v in data.items()}

    return {'statusCode': 200,
            'body': json.dumps(data, default=utilities.decimal_default),
            'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": "*"}}
