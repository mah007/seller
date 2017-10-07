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

def getOrder():
	user = {
		'lazada_api_key': 'jusjWjdv13rre3RxH9b-cXmmA7B9cQQh4jtiLcDyAqX-8PMkhutFeRsv',
		'lazada_user_id': 'info@zakos.vn'
	}
	order = {
		'id': '111682924'
	}

	customer = OrderManager()
	result = customer.getOrder(order, user)
	return make_response(jsonify(result))


# ------------------------------------------------------------------------------
# Get Order Item
# ------------------------------------------------------------------------------
@OrderAPI.route('/order/get-order-items', methods=['GET'])
@cross_origin()
def getOrderItems():
	user = {
		'lazada_api_key': 'jusjWjdv13rre3RxH9b-cXmmA7B9cQQh4jtiLcDyAqX-8PMkhutFeRsv',
		'lazada_user_id': 'info@zakos.vn'
	}
	# 111677474, 111618240, 111682924
	order = {
		'id': '111682924'
	}

	orderItems = OrderManager()
	result = orderItems.getOrderItems(order, user)

	return make_response(jsonify(result))


@OrderAPI.route('/order/get-failed-orders', methods=['GET'])
@cross_origin()
def getFailedOrders():
	user = {
		'user_id': 'lakami',
		'lazada_api_key': 'jusjWjdv13rre3RxH9b-cXmmA7B9cQQh4jtiLcDyAqX-8PMkhutFeRsv',
		'lazada_user_id': 'info@zakos.vn'
	}

	orderManager = OrderManager()
	# Check condition constant. Then insert result to database
	orderManager.insertOrderFromLazadaWithOneUser(user)

	result = orderManager.getAllFailedOrders()

	if 'success' in result:
		return make_response(jsonify(result))
	else:
		return make_response(jsonify({"error": "There is no order here"}))

@OrderAPI.route('/order/update-order', methods=['POST'])
@cross_origin()
def updateOrderState():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not request.json:
		return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
	if not 'id' in request.json:
		return make_response(jsonify({'error': 'Missing json parameter'}), 404)

	order = {
		"id": request.json['id'],
	}
	orderManager = OrderManager()
	result = orderManager.updateOrderState(order, request.args.get('token'))

	if 'success' in result:
		return make_response(jsonify({"success": "done"}))
	else:
		return make_response(jsonify(result))

# ------------------------------------------------------------------------------
# Set order status to ready-to-ship
# ------------------------------------------------------------------------------
@OrderAPI.route('/order/ready-to-ship', methods=['POST'])
@cross_origin()
def setStatusToReadyToShip():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	token = request.args.get('token');
	if not token:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not request.json:
		return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
	if not 'orderItemIds' in request.json:
		return make_response(jsonify({'error': 'Missing orderItemIds parameter value'}), 404)
	if not 'shippingProvider' in request.json:
		return make_response(jsonify({'error': 'Missing shippingProvider parameter value'}), 404)

	orderItemIds = request.json['orderItemIds']
	shippingProvider = request.json['shippingProvider']
	orderManager = OrderManager()
	result = orderManager.setStatusToReadyToShip(token, orderItemIds, shippingProvider)
	if 'success' in result:
		return make_response(jsonify(result), 201)
	else:
		return make_response(jsonify(result), 404)













