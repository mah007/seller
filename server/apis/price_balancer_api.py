import time
import simplejson as json
from flask_cors import CORS, cross_origin
from flask import Blueprint, render_template, abort, request, make_response, jsonify
from managers.price_balancer_manager import PriceBalancerManager
from lazada_api.lazada_order_api import LazadaOrderApi
from utils.timestamp_utils import TimestampUtils


PriceBalacerAPI = Blueprint('price_balancer_api', __name__, template_folder='apis')

# ------------------------------------------------------------------------------
# Insert price balancer
# ------------------------------------------------------------------------------
@PriceBalacerAPI.route('/price-balancer/insert', methods=['POST'])
@cross_origin()
def insert():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not request.json:
		return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
	if not request.json:
		return make_response(jsonify({'error': 'Missing username parameters value'}), 404)
	if not 'sku' in request.json:
		return make_response(jsonify({'error': 'Missing sku parameter'}), 404)
	if not 'name' in request.json:
		return make_response(jsonify({'error': 'Missing min_price parameter'}), 404)
	if not 'url' in request.json:
		return make_response(jsonify({'error': 'Missing max_price parameter'}), 404)
	if not 'current_price' in request.json:
		return make_response(jsonify({'error': 'Missing compete_price parameter'}), 404)
	if not 'price_by_time' in request.json:
		return make_response(jsonify({'error': 'Missing state parameter'}), 404)

	priceBalancer = {
		"sku": request.json['sku'],
		"name": "null",
		"url": "null",
		"current_price": int(request.json['min_price']),
		"price_by_time": int(request.json['max_price'])
	}

	priceBalancerManager = PriceBalancerManager()
	result = priceBalancerManager.insert(priceBalancer, request.args.get('token'))
	if 'success' in result:
		return make_response(json.dumps(sku), 201)
	else:
		return make_response(jsonify(result), 404)










