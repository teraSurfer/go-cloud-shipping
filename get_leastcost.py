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

    # If source and destination divisions are passed
    # then return the current least shipment cost for given
    # source and destination divisions.
    if event[PARAMS]:
        source_division = event[PARAMS][SOURCE_DIVISION_KEY]
        destination_division = event[PARAMS][DESTINATION_DIVISION_KEY]
        for item in data:
            if item['SourceDivision'] == source_division:
                data = {'least_price': item[destination_division]['Price']}
                break
    else:
        data = {'least_price': list(data)}

    return {'statusCode': 200,
            'body': json.dumps(data, default=utilities.decimal_default),
            'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": "*"}}
