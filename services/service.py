import json
import os
from persistence.persistence import Persistence
from models.model import Models

class Service:
    def __init__(self):
        self.db = Persistence()
        self.url = os.environ['url']
        self.model = Models()
        
    def get_data_categories(self):
        type_shoes = self.db.get_shoes_categories()
        type_sub_rutes = {type_shoe: f'{self.url}{type_shoe}' for type_shoe in type_shoes}
        return type_sub_rutes
    
    def get_data_shoes_for_categories(self, category):
        data_shoes = self.db.get_shoes(category)
        [shoe.update({'canonicalProductURL': f'{self.url}{shoe["idShoe"]}'}) for shoe in data_shoes]
        response = self.model.get_model_response(data_shoes)
        return response

    def get_shoe_data(self, id):
        data_shoe = self.db.get_shoe(id)
        del data_shoe['canonicalProductURL']
        return data_shoe

    def create_order_shoes(self, params):
        response = self.db.create_order(params)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return 'Se registraron los datos de manera correcta'
        else:
            return 'Algo salio mal con tu pedido'

    def get_orders_for_user(self, user):
        response = self.db.get_orders(user)
        if len(response) > 0:
            return self.model.get_model_response(response)
        else:
            return 'No encontramos valores'
    
    def service_shoes(self, event, context):
        method = event['httpMethod']
        path = event['path'].split('/')
        if len(path) > 2 and path[2] != 0:
            data = lambda param: self.get_shoe_data(param) if param.isnumeric() else self.get_data_shoes_for_categories(param)  
            return data(path[2])
        else:
            return self.get_data_categories()
            
    def service_orders(self, event, context):
        method = event['httpMethod']
        if method == 'POST':
            body = json.loads(event['body'])
            return self.create_order_shoes(body)
        else:
            path = event['path'].split('/')
            return self.get_orders_for_user(path[2])
            