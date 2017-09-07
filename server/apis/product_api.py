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
	productManager.insertProductFromLazada(request.args.get('token'))
	result = productManager.getAllProduct(request.args.get('token'))

	if 'success' in result:
		return make_response(jsonify(result), 201)
	else:
		return make_response(jsonify(result), 404)

