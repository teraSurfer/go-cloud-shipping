import json
from util.constants import *
from util import utilities
import os
import decimal

dynamodb = None

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def handler(event, context):
    global dynamodb
    if not dynamodb:
        dynamodb = utilities.get_dynamodb_client(event)

    table = dynamodb.Table(LOCATIONS_TABLE)
    response = table.scan()

    items = response['Items']
    divisions = set()
    for item in items:
        divisions.add(item[DIVISION_COLUMN])

    return {'statusCode': 200,
            'body': json.dumps(divisions, default=utilities.set_default),
            'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": "*"}}
