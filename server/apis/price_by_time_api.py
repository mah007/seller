import simplejson as json
from flask_cors import CORS, cross_origin
from flask import Blueprint, render_template, abort, request, make_response, jsonify
from managers.price_by_time_manager import PriceByTimeManager
from controllers.product.product_controller import ProductController


PriceByTimeAPI = Blueprint('price_by_time_api', __name__, template_folder='apis')

# ------------------------------------------------------------------------------
# Insert price balancer
# ------------------------------------------------------------------------------
@PriceByTimeAPI.route('/price-by-time/insert', methods=['POST'])
@cross_origin()
def insertPriceByTime():
  if not request.args:
    return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
  if not request.json:
    return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
  if not 'token' in request.args:
    return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
  if not 'sku' in request.json:
    return make_response(jsonify({'error': 'Missing json parameter'}), 404)
  if not 'price_by_time' in request.json:
    return make_response(jsonify({'error': 'Missing json parameter'}), 404)

  sku = {
    "sku": request.json['sku'],
    "price_by_time": request.json['price_by_time']
  }

  priceByTimeManager = PriceByTimeManager()
  result = priceByTimeManager.insert(sku, request.args.get('token'))
  if 'success' in result:
    return make_response(jsonify(result), 201)
  else:
    return make_response(jsonify(result), 404)

# ------------------------------------------------------------------------------
# Delete a price balancer
# ------------------------------------------------------------------------------
@PriceByTimeAPI.route('/price-by-time/delete', methods=['POST'])
@cross_origin()
def deletePriceByTime():
  if not request.args:
    return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
  if not request.json:
    return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
  if not 'token' in request.args:
    return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
  if not 'id' in request.json:
    return make_response(jsonify({'error': 'Missing json parameter'}), 404)

  sku = {"id": request.json['id']}

  priceByTimeManager = PriceByTimeManager()
  result = priceByTimeManager.delete(sku, request.args.get('token'))
  if 'success' in result:
    return make_response(jsonify(result), 201)
  else:
    return make_response(jsonify(result), 404)

# ------------------------------------------------------------------------------
# Update a price balancer
# ------------------------------------------------------------------------------
@PriceByTimeAPI.route('/price-by-time/update', methods=['POST'])
@cross_origin()
def updatePriceByTime():
  if not request.args:
    return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
  if not request.json:
    return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
  if not 'token' in request.args:
    return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
  if not 'id' in request.json:
    return make_response(jsonify({'error': 'Missing json parameter'}), 404)
  if not 'price_balance' in request.json:
    return make_response(jsonify({'error': 'Missing json parameter'}), 404)

  sku = {
    "id": request.json['id'],
    "price_balance": request.json['price_balance']
  }

  priceByTimeManager = PriceByTimeManager()
  result = priceByTimeManager.update(sku, request.args.get('token'))
  if 'success' in result:
    return make_response(jsonify(result), 201)
  else:
    return make_response(jsonify(result), 404)

# ------------------------------------------------------------------------------
# Get all skus of price balancer
# ------------------------------------------------------------------------------
@PriceByTimeAPI.route('/price-by-time/get-all', methods=['GET'])
@cross_origin()
def getAllSkuOfPriceByTime():
  if not request.args:
    return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
  if not 'token' in request.args:
    return make_response(jsonify({'error': 'Missing token parameter value'}), 404)


  priceByTimeManager = PriceByTimeManager()
  result = priceByTimeManager.getAll(request.args.get('token'))
  if 'success' in result:
    return make_response(jsonify(result), 201)
  else:
    return make_response(jsonify(result), 404)

# ------------------------------------------------------------------------------
# Search Product by name, seller sku, shop sku, brand and model
# ------------------------------------------------------------------------------
@PriceByTimeAPI.route('/price-by-time/search', methods=['POST'])
@cross_origin()
def searchProduct():
  if not request.args:
    return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
  if not request.json:
    return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
  if not 'token' in request.args:
    return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
  if not 'search_key' in request.json:
    return make_response(jsonify({'error': 'Missing json parameter'}), 404)

  searchKey = request.json['search_key']
  token = request.args.get('token')
  productCtrl = ProductController()
  result = productCtrl.searchProduct(token, searchKey)
  if 'success' in result:
    return make_response(jsonify(result), 201)
  else:
    return make_response(jsonify(result), 404)











