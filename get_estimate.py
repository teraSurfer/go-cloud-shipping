import boto3
import json
from util.constants import *
from util import utilities
import os

dynamodb = None

def handler(event, context):
    global dynamodb
    if not dynamodb:
        dynamodb = utilities.get_dynamodb_client(event)

    price_and_vendor = utilities.get_least_price_and_vendor(dynamodb, event[PARAMS]['origin'], event[PARAMS]['destination'])

    result = {'price': str(int(price_and_vendor[PRICE_COLUMN] * int(event[PARAMS]['weight'])))}

    return {'statusCode': 200,
            'body': json.dumps(result),
            'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": "*"}}
