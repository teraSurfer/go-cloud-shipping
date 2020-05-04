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

    response = None
    if body.get('customer'):
        table = dynamodb.Table(USERS_TABLE)

        response = table.get_item(
            Key={
                U_EMAIL_COLUMN: body['email']
            }
        )
    else:
        table = dynamodb.Table(VENDORS_TABLE)

        response = table.get_item(
            Key={
                V_EMAIL_COLUMN: body['email']
            }
        )

    if response.get('Item') is None:
            return {'statusCode': 201,
                    'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}}
    else:
        if response.get('Item').get(PASSWORD) == body['password']:
            return {'statusCode': 200,
                'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": "*"}}
        else:
            return {'statusCode': 201,
                    'headers': {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "*"}}
