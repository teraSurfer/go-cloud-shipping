import boto3
import json
from util.constants import *
from util import utilities
import os
import time
from datetime import date

dynamodb = None

def handler(event, context):
    global dynamodb
    if not dynamodb:
        dynamodb = utilities.get_dynamodb_client(event)

    print(event)
    body = json.loads(event['body'])
    table = dynamodb.Table(VENDORS_TABLE)

    response = table.get_item(
        Key={
            U_EMAIL_COLUMN: body['v_email']
        }
    )

    if response.get('Item'):
        response = table.put_item(
            Item ={
                V_EMAIL_COLUMN: body['v_email'],
                V_NAME_COLUMN: body['name'],
                V_MOBILE_COLUMN: int(body['mobile'])
            }
        )

    return {'statusCode': 200,
            'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": "*"}}
