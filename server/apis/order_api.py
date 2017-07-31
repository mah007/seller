import time
import simplejson as json
from flask_cors import CORS, cross_origin
from flask import Blueprint, render_template, abort, request, make_response, jsonify
from lazada_api.lazada_order_api import LazadaOrderApi
from managers.order_manager import OrderManager

OrderAPI = Blueprint('order_api', __name__, template_folder='apis')


# ------------------------------------------------------------------------------
# Get Order
# ------------------------------------------------------------------------------
@OrderAPI.route('/order/get-order', methods=['GET'])
@cross_origin()
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