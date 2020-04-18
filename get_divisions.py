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

    # table = dynamodb.Table(LOCATIONS_TABLE)
    # response = table.scan()
    #
    # items = response['Items']
    # divisions = set()
    # for item in items:
    #     divisions.add(item[DIVISION_COLUMN])

    divisions = {"divisions":[CENTRAL1_COLUMN, CENTRAL2_COLUMN, EAST1_COLUMN,EAST2_COLUMN, NORTH1_COLUMN, NORTH2_COLUMN,
                              NORTH3_COLUMN,    NORTHEAST1_COLUMN,   NORTHEAST2_COLUMN, SOUTH1_COLUMN, SOUTH2_COLUMN,
                              SOUTH3_COLUMN,  WEST1_COLUMN, WEST2_COLUMN  ]}
    return {'statusCode': 200,
            'body': json.dumps(divisions, default=utilities.set_default),
            'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": "*"}}
