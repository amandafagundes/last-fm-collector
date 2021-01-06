import boto3
import os

dynamodb_client = boto3.client('dynamodb', region_name="us-east-1")
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

class Database:

    def getUsersId(self):
        rawData = table.scan(
            Select='SPECIFIC_ATTRIBUTES',
            AttributesToGet=['user_id', 'created_at'])

        if(rawData == None):
            return []
        return rawData['Items']

    def save(self, item):
        table.put_item(Item=item)

