import time
import simplejson as json
from flask_cors import CORS, cross_origin
from flask import Blueprint, render_template, abort, request, make_response, jsonify
from lazada_api.lazada_order_api import LazadaOrderApi


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

	customer = LazadaOrderApi()
	result = customer.getOrder(order, user)
	return make_response(result)