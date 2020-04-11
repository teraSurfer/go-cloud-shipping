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

    response  = None
    type = event[PARAMS]['type']
    if type == 'vendor':
        response = table.scan(
            FilterExpression= Key(V_EMAIL_COLUMN).eq(event[PARAMS]['v_email'])
        )
    else:
        response = table.scan(
            FilterExpression= Key(U_EMAIL_COLUMN).eq(event[PARAMS]['u_email'])
        )

    data =response['Items']


    return {'statusCode': 200,
            'body': json.dumps(data, default=utilities.decimal_default),
            'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": "*"}}
