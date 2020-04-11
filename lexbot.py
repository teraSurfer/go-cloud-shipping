
from util.constants import *
from util import utilities
import os
from boto3.dynamodb.conditions import Key, Attr

import boto3

dynamodb = None
def handler(event, context):
    global dynamodb
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    price_and_vendor = utilities.get_least_price_and_vendor(dynamodb, int(event['currentIntent']['slots']['Source']), int(event['currentIntent']['slots']['Destination']))

    result = {'price': int(price_and_vendor[PRICE_COLUMN] * int(event['currentIntent']['slots']['Weight']))}

    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "SSML",
                "content": "Estimated cost of your shipment is Rs." + str(result['price']) + ". Please login to place shipment order. Thank you for visiting SysteamBiz."
            },
        }
    }
    print('result = ' + str(response))
    return response