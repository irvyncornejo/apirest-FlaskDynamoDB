from flask import Flask
from flask import request
from flask import jsonify
import json
from services.service import Service


app = Flask(__name__)
service = Service()
""""
- GET
    /tenis
    tenis/categoria
    tenis/categoria/id
    ---
    /ordenes/user_id

-POST
    ORDER

"""

@app.route('/api/tenis')
def get_categories():
    types = service. get_data_categories()
    return json.dumps(types)

@app.route('/api/tenis/<string:category_shoes>')
def get_shoes_for_category(category_shoes):
    types = service.get_data_shoes_for_categories(category_shoes)
    return jsonify(types)

@app.route('/api/tenis/<int:id>')
def get_shoe_data(id):
    shoe_data = service.get_shoe_data(id)
    return jsonify(shoe_data)

@app.route('/api/ordenes', methods=['POST'])
def create_orden():
    response = service.create_order_shoes(request.json)
    return response

@app.route('/api/ordenes/<string:user>')
def get_orders_user(user):
    response = service.get_orders_for_user(user)
    return response

app.run(debug=True)