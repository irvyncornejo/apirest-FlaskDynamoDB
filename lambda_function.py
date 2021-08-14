import json
from services.service import Service

def define_rute(event, context):
    service = Service()
    
    method = event['httpMethod']
    path = event['path']
    
    if ('tenis' in path and method == 'GET'):
        response = service.service_shoes(event, context)
        return response
    if 'ordenes' in path and (method == 'GET' or method == 'POST'):
        response = service.service_orders(event, context)
        return response
    else:
        return 'Valida que los valores ingresados con corresctos'

def lambda_handler(event, context):
    try:
        response = define_rute(event, context)
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    
    except Exception as e:
        print(e)
        return{
            'statusCode': 500,
            'body': 'Tenemos un error al procesar tu solicitud'
        }