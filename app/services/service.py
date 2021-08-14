from persistence.persistence import Persistence
import json

class Service:
    def __init__(self):
        self.db = Persistence()
        self.end_point = 'http://127.0.0.1:5000/api/tenis/'
    def get_data_categories(self):
        type_shoes = self.db.get_shoes_categories()
        type_sub_rutes = {type_shoe: f'{self.end_point}/{type_shoe}' for type_shoe in type_shoes}
        return type_sub_rutes
    
    def get_data_shoes_for_categories(self, category):
        data_shoes = self.db.get_shoes(category)
        [shoe.update({'canonicalProductURL': f'{self.end_point}{shoe["idShoe"]}'}) for shoe in data_shoes]
        response = {
            'info': {
                'count': str(len(data_shoes))
                },
            'results': data_shoes
        }
        return response

    def get_shoe_data(self, id):
        data_shoe = self.db.get_shoe(id)
        del data_shoe['canonicalProductURL']
        return data_shoe

    def create_order_shoes(self, params):
        response = self.db.create_order(params)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return 'Solicitud envíada para los datos'
        else:
            return 'Algo salio mal con tu pedido'

    def get_orders_for_user(self, user):
        response = self.db.get_orders(user)
        if len(response) > 0:
            return json.dumps(response)
        else:
            return 'No encontramos valores'