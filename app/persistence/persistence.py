import datetime
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
from botocore.config import Config

class Persistence:
    def __init__(self, dynamodb=None):
        if not dynamodb:
            my_config=Config(
                region_name = 'us-west-2',
                signature_version = 'v4',
            )
            self.dynamodb = boto3.client('dynamodb', region_name='us-west-2',aws_access_key_id='fake',aws_secret_access_key='fake',endpoint_url='http://dynamodb-local:8000')
            self.resource_db = boto3.resource('dynamodb',  region_name='us-west-2',aws_access_key_id='fake',aws_secret_access_key='fake',endpoint_url='http://dynamodb-local:8000')
        self.table = lambda name: self.resource_db.Table(name)

    def get_shoes_categories(self):
        done = False
        start_key = None
        type_shoes = list()
        while not done:
            table = self.table('Shoes')
            response = table.scan()
            [type_shoes.append(shoe['typeShoe']) for shoe in response.get('Items',[]) if not shoe['typeShoe'] in type_shoes]
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None
        return type_shoes

    def get_shoes(self, category):
        done = False
        start_key = None
        scan_kwars = {
                'FilterExpression': Key('typeShoe').eq(category)
            }
        while not done:
            table = self.table('Shoes')
            response = table.scan(**scan_kwars)
            shoes = response.get('Items',[])
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None
        return shoes

    def get_shoe(self, id):
        table = self.table('Shoes')
        response = table.query(
            KeyConditionExpression=Key('idShoe').eq(str(id))
        )
        return response['Items'][0]

    def create_order(self, data):
        table = self.table('Orders')
        now = datetime.now()
        response = table.put_item(
            Item={
                'user': data['user'],
                'idOrder': now.strftime('%d%m%Y-%H%M%S'),
                'shoes': data['shoes']
            }
        )
        return response

    def get_orders(self, user):
        table = self.table('Orders')
        response = table.query(
            KeyConditionExpression=Key('user').eq(user)
        )
        return response['Items']