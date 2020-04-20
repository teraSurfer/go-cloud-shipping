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

    if event[PARAMS].get('v_email'):
        response = table.scan(
            FilterExpression= Key(V_EMAIL_COLUMN).eq(event[PARAMS]['v_email'])
        )
    else:
        response = table.scan(
            FilterExpression= Key(U_EMAIL_COLUMN).eq(event[PARAMS]['u_email'])
        )

    new_orders = []
    for order in response['Items']:
        new_order = {}
        for k,v in order.items():
            new_order[k.lower()] = v
        new_orders.append(new_order)

    orders = {"orders": new_orders}

    return {'statusCode': 200,
            'body': json.dumps(orders, default=utilities.decimal_default),
            'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": "*"}}
