class Models:
    def get_model_tables(self):
        return {
            'shoes':{
                'TableName':'Shoes',
                'KeySchema':[
                    {
                        'AttributeName': 'idShoe',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'typeShoe',
                        'KeyType': 'RANGE'
                    }
                ],
                'AttributeDefinitions':[
                    {
                        'AttributeName': 'idShoe',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'typeShoe',
                        'AttributeType': 'S'
                    },
                ]
            },
            'orders':{
                'TableName':'Orders',
                'KeySchema':[
                    {
                        'AttributeName': 'user',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'idOrder',
                        'KeyType': 'RANGE'
                    }
                ],
                'AttributeDefinitions':[
                    {
                        'AttributeName': 'user',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'idOrder',
                        'AttributeType': 'S'
                    },
                ]
            },}
