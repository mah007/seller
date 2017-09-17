import time
import simplejson as json
from flask_cors import CORS, cross_origin
from flask import Blueprint, render_template, abort, request, make_response, jsonify
from managers.product_manager import ProductManager
from lazada_api.lazada_order_api import LazadaOrderApi
from utils.timestamp_utils import TimestampUtils


ProductAPI = Blueprint('product_api', __name__, template_folder='apis')

# ------------------------------------------------------------------------------
# Get Product
# ------------------------------------------------------------------------------
@ProductAPI.route('/product/get', methods=['GET'])
@cross_origin()
def getAllProduct():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not 'token' in request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)

	productManager = ProductManager()
	# productManager.insertProductFromLazada(request.args.get('token'))

	result = productManager.getAllProduct(request.args.get('token'))

	if 'success' in result:
		return make_response(jsonify(result), 201)
	else:
		return make_response(jsonify(result), 404)


# ------------------------------------------------------------------------------
# Update Product (contain quantity and price)
# ------------------------------------------------------------------------------
@ProductAPI.route('/product/update', methods=['POST'])
@cross_origin()
def updateProduct():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not request.json:
		return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
	if not 'quantity' in request.json:
		return make_response(jsonify({'error': 'Missing json parameter'}), 404)
	if not 'price' in request.json:
		return make_response(jsonify({'error': 'Missing json parameter'}), 404)
	if not 'id' in request.json:
		return make_response(jsonify({'error': 'Missing state parameter'}), 404)

	newValue = {
		"id": request.json['id'],
		"price": request.json['price'],
		"quantity": request.json['quantity']
	}

	productManager = ProductManager()
	result = productManager.updateProduct(newValue, request.args.get('token'))
	if 'success' in result:
		return make_response(jsonify({"success": "done"}), 201)
	else:
		return make_response(jsonify(result), 404)


# ------------------------------------------------------------------------------
# Update Product quantity
# ------------------------------------------------------------------------------
@ProductAPI.route('/product/update-quantity', methods=['POST'])
@cross_origin()
def updateProductQuantity():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not request.json:
		return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
	if not 'quantity' in request.json:
		return make_response(jsonify({'error': 'Missing json parameter'}), 404)
	if not 'id' in request.json:
		return make_response(jsonify({'error': 'Missing state parameter'}), 404)

	newValue = {
		"id": request.json['id'],
		"quantity": request.json['quantity']
	}

	productManager = ProductManager()
	result = productManager.updateProductQuantity(newValue, request.args.get('token'))
	if 'success' in result:
		return make_response(jsonify({"success": "done"}), 201)
	else:
		return make_response(jsonify(result), 404)

# ------------------------------------------------------------------------------
# Update Product price
# ------------------------------------------------------------------------------
@ProductAPI.route('/product/update-price', methods=['POST'])
@cross_origin()
def updateProductPrice():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not request.json:
		return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
	if not 'price' in request.json:
		return make_response(jsonify({'error': 'Missing state parameter'}), 404)
	if not 'id' in request.json:
		return make_response(jsonify({'error': 'Missing state parameter'}), 404)

	newValue = {
		"id": request.json['id'],
		"price": request.json['price']
	}

	productManager = ProductManager()
	result = productManager.updateProductPrice(newValue, request.args.get('token'))
	if 'success' in result:
		return make_response(jsonify({"success": "done"}), 201)
	else:
		return make_response(jsonify(result), 404)


