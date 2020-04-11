import json
from util.constants import *
from util import utilities


import os

dynamodb = None

def handler(event, context):
    global dynamodb
    if not dynamodb:
        dynamodb = utilities.get_dynamodb_client(event)

    table = dynamodb.Table(PRICES_TABLE)
    response = table.scan()
    data = response['Items']
    print(data)

    return {'statusCode': 200,
            'body': json.dumps(data, default=utilities.decimal_default),
            'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": "*"}}
