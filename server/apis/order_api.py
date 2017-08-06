import time
import simplejson as json
from flask_cors import CORS, cross_origin
from flask import Blueprint, render_template, abort, request, make_response, jsonify
from lazada_api.lazada_order_api import LazadaOrderApi
from managers.order_manager import OrderManager

OrderAPI = Blueprint('order_api', __name__, template_folder='apis')

# ------------------------------------------------------------------------------
# Scan barcode
# ------------------------------------------------------------------------------
@OrderAPI.route('/order/scan-barcode', methods=['POST'])
@cross_origin()
def scanBarcode():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not request.json:
		return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
	if not 'barcode' in request.json:
		return make_response(jsonify({'error': 'Missing json parameter value'}), 404)

	orderManager = OrderManager()
	result = orderManager.scanBarcode(request.args.get('token'), request.json['barcode'])
	if 'success' in result:
		return make_response(jsonify(result), 201)
	else:
		return make_response(jsonify(result), 404)


# ------------------------------------------------------------------------------
# Refresh all order
# ------------------------------------------------------------------------------
@OrderAPI.route('/order/refresh-all-orders', methods=['GET'])
@cross_origin()
def refreshAllOrders():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	token = request.args.get('token');
	if not token:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)

	orderManager = OrderManager()
	result = orderManager.refreshAllOrders(token)
	if 'success' in result:
		return make_response(jsonify(result), 201)
	else:
		return make_response(jsonify(result), 404)












