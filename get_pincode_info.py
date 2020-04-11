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

    table = dynamodb.Table(LOCATIONS_TABLE)
    response = table.get_item(
        Key={
            PINCODE_COLUMN: int(event[PARAMS]['pincode'])
        }
    )

    if response.get('Item') is None:
        return {'statusCode': 404, 'headers': {'Content-Type': 'application/json'}}
    else:
        item = response['Item']

        result = {}

        result['brnm'] = item[BRNM_COLUMN]
        result['area'] = item[AREA_COLUMN]

        return {'statusCode': 200,
                'body': json.dumps(result),
                'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": "*"}}
