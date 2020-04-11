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
    table = dynamodb.Table(USERS_TABLE)

    response = table.get_item(
        Key={
            U_EMAIL_COLUMN: body['u_email']
        }
    )

    if response.get('Item') is None:
        response = table.put_item(
            Item ={
                U_EMAIL_COLUMN: body['u_email'],
                FIRST_NAME_COLUMN: body['first_name'],
                LAST_NAME_COLUMN: body['last_name']
            }
        )

    return {'statusCode': 200,
            'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": "*"}}
