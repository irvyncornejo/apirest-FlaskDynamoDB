from requests.api import delete
import boto3
import subprocess as sp
from ..services.model import Models
from ..services.extract import Scraper
from time import sleep
class Persistence:
    def __init__(self, dynamodb=None):
        if not dynamodb:
            self.dynamodb = boto3.client('dynamodb', region_name='us-west-2',aws_access_key_id='fake',aws_secret_access_key='fake',endpoint_url='http://dynamodb-local:8000')
            self.resource_db = boto3.resource('dynamodb', region_name='us-west-2',aws_access_key_id='fake',aws_secret_access_key='fake',endpoint_url='http://dynamodb-local:8000')
    
    def create_tables(self, tables):
        tables_name_dynamo = self.dynamodb.list_tables(ExclusiveStartTableName='string',Limit=10)['TableNames']
        try:
            for table in tables:
                print(table)
                value = tables[table]
                if not(value['TableName']) in tables_name_dynamo or len(tables_name_dynamo)==0:
                    self.dynamodb.create_table(
                        TableName = value['TableName'],
                        KeySchema= value['KeySchema'],
                        AttributeDefinitions= value['AttributeDefinitions'],
                        ProvisionedThroughput={
                            'ReadCapacityUnits': 10,
                            'WriteCapacityUnits': 10
                        }
                    )
            
        except Exception as e:
            print(e)
            return e

    def define_data_shoe(self, raw_data):
        return {
            'idShoe': raw_data['idShoe'],
            'typeShoe': raw_data['typeShoe'],
            'productName': raw_data['productName'],
            'prLocale': raw_data['prLocale'],
            'merchantGroupId': raw_data['merchantGroupId'],
            'merchantId': raw_data['merchantId'],
            'productLongDescription': raw_data['productLongDescription'],
            'canonicalProductURL': raw_data['canonicalProductURL'],
            'metaImageURL': f'https:{raw_data["metaImageURL"]}',
            'seoCategoryName': raw_data['seoCategoryName'],
            'ogPrice': str(raw_data['ogPrice']),
            'tallas': [{'34': '100'}, {'34.5': '100'}, {'35':'10'}, {'36':'5'}, {'40':'2'}]
        }
    def insert_data_shoes(self):
        table = self.resource_db.Table('Shoes')
        data = Scraper().get_data_shoes()
        data_shoes = [self.define_data_shoe(shoe) for shoe in data]
        for shoe in data_shoes:
            table.put_item(Item=shoe)

    def delete_tables(self, names):
        for name in names:
            self.resource_db.Table(name).delete()
    
    def main(self):
        tables = Models().get_model_tables()
        db = Persistence()
        #db.delete_tables(['Shoes'])
        db.create_tables(tables)
        db.insert_data_shoes()
    