import boto3
import json
from util.constants import *
from util import utilities
import os
import time
from datetime import datetime

from datetime import date

dynamodb = None

def handler(event, context):
    global dynamodb
    if not dynamodb:
        dynamodb = utilities.get_dynamodb_client(event)

    print(event)
    body = json.loads(event['body'])

    price_and_vendor = utilities.get_least_price_and_vendor(dynamodb, body['origin'], body['destination'])
    id = int(round(time.time() * 1000))
    price = int(price_and_vendor[PRICE_COLUMN] * int(body['weight']))

    result = {'price': price,
              'id': id,
              'v_email': price_and_vendor[V_EMAIL_COLUMN],
              'status' : 'Accepted'
     }


    table = dynamodb.Table(VENDORS_TABLE)

    response = table.get_item(
        Key={
            V_EMAIL_COLUMN : price_and_vendor[V_EMAIL_COLUMN]
        }
    )

    result['v_name'] = response['Item'][V_NAME_COLUMN]
    result['v_mobile'] = response['Item'][V_MOBILE_COLUMN]

    table = dynamodb.Table(ORDERS_TABLE)

    response = table.put_item(
        Item ={
            ID_COLUMN: int(id),
            U_EMAIL_COLUMN: body['u_email'],
            ORIGIN_COLUMN : body['origin'],
            DESTINATION_COLUMN: body['destination'],
            O_ADDRESS_COLUMN: body['o_address'],
            D_ADDRESS_COLUMN: body['d_address'],
            PRICE_COLUMN: int(price),
            V_EMAIL_COLUMN: price_and_vendor[V_EMAIL_COLUMN],
            WEIGHT_COLUMN: int(body['weight']),
            O_MOBILE_COLUMN: int(body['o_mobile']),
            D_MOBILE_COLUMN: int(body['d_mobile']),
            O_DATE_COLUMN: str(datetime.fromtimestamp(time.time())),
            P_DATE_COLUMN: body['p_date'],
            STATUS_COLUMN: 'Accepted',
            V_NAME_COLUMN: result['v_name'],
            V_MOBILE_COLUMN: result['v_mobile']
        }
    )

    return {'statusCode': 200,
            'body': json.dumps(result, default=utilities.decimal_default),
            'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": "*"}}
