import time
import simplejson as json
from flask_cors import CORS, cross_origin
from flask import Blueprint, render_template, abort, request, make_response, jsonify
from managers.price_balancer_manager import PriceBalancerManager
from lazada_api.lazada_order_api import LazadaOrderApi
from utils.timestamp_utils import TimestampUtils


PriceBalancerAPI = Blueprint('price_balancer_api', __name__, template_folder='apis')

# ------------------------------------------------------------------------------
# Insert price balancer
# ------------------------------------------------------------------------------
@PriceBalancerAPI.route('/price-balancer/insert', methods=['POST'])
@cross_origin()
def insertPriceBalancer():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not request.json:
		return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
	if not request.json:
		return make_response(jsonify({'error': 'Missing username parameters value'}), 404)
	if not 'sku' in request.json:
		return make_response(jsonify({'error': 'Missing sku parameter'}), 404)
	if not 'name' in request.json:
		return make_response(jsonify({'error': 'Missing name parameter'}), 404)
	if not 'url' in request.json:
		return make_response(jsonify({'error': 'Missing url parameter'}), 404)
	if not 'current_price' in request.json:
		return make_response(jsonify({'error': 'Missing current price parameter'}), 404)
	if not 'price_time' in request.json:
		return make_response(jsonify({'error': 'Missing price by time parameter'}), 404)

	priceBalancer = {
		"sku": request.json['sku'],
		"name": request.json['name'],
		"url": request.json['url'],
		"current_price": int(request.json['current_price']),
		"price_by_time": int(request.json['price_time'])
	}

	priceBalancerManager = PriceBalancerManager()
	result = priceBalancerManager.insert(priceBalancer, request.args.get('token'))
	if 'success' in result:
		return make_response(json.dumps(priceBalancer), 201)
	else:
		return make_response(jsonify(result), 404)

# ------------------------------------------------------------------------------
# Delete Price Balancer
# ------------------------------------------------------------------------------
# @PriceBalancerAPI.route('/price-balancer/delete', methods=['POST'])
# @cross_origin()
# def delete():
# 	if not request.args:
# 		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
# 	if not request.json:
# 		return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
# 	if not 'id' in request.json:
# 		return make_response(jsonify({'error': 'Missing json parameter'}), 404)

# 	priceBalancer = {
# 		"id": request.json['id']
# 	}

# 	priceBalancerManager = PriceBalancerManager()
# 	result = priceBalancerManager.delete(priceBalancer, request.args.get('token'))
# 	if 'success' in result:
# 		return make_response(jsonify({"success": "done"}), 201)
# 	else:
# 		return make_response(jsonify(result), 404)











