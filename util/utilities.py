import boto3
import decimal
from util.constants import *

def get_dynamodb_client(event):
    dynamodb = None

    if event['requestContext']['identity']['sourceIp'] == '127.0.0.1':
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://host.docker.internal:8000")
    else:
        dynamodb = boto3.resource('dynamodb')

    return dynamodb

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return int(obj)
    raise TypeError

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError



def get_least_price_and_vendor(dynamodb, origin, destination):

    table = dynamodb.Table(LOCATIONS_TABLE)
    response = table.get_item(
        Key={
            PINCODE_COLUMN: int(origin)
        }
    )

    origin_division = response['Item'][DIVISION_COLUMN]

    table = dynamodb.Table(LOCATIONS_TABLE)
    response = table.get_item(
        Key={
            PINCODE_COLUMN: int(destination)
        }
    )

    destination_division = response['Item'][DIVISION_COLUMN]

    table = dynamodb.Table(PRICES_TABLE)
    response = table.get_item(
        Key={
            SOURCE_DIVISION_COLUMN: origin_division
        }
    )

    price_and_vendor = response['Item'][destination_division]

    return price_and_vendor