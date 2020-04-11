import json

import boto3
import json
from util import utilities

def handler(event, context):

    body = json.loads(event['body'])

    client = boto3.client('lex-runtime')
    response = client.post_text(
        botName='Estimate',
        botAlias='lex',
        userId=body['user'],
        sessionAttributes={
            'string': 'string'
        },
        requestAttributes={
            'string': 'string'
        },
        inputText=body['message']
    )

    print(response)

    return {'statusCode': 200,
            'body': json.dumps(response, default=utilities.decimal_default),
            'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin": "*"}}
