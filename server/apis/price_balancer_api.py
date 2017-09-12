from managers.price_balancer_manager import PriceBalancerManager


SkuAPI = Blueprint('price_balancer_api', __name__, template_folder='apis')

# ------------------------------------------------------------------------------
# Insert price balancer
# ------------------------------------------------------------------------------
@SkuAPI.route('/price-balancer/insert', methods=['POST'])
@cross_origin()
def insertPriceBalancer():
  if not request.args:
    return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
  if not 'token' in request.args:
    return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
  if not 'sku' in request.json:
    return make_response(jsonify({'error': 'Missing json parameter'}), 404)
  if not 'price_balance' in request.json:
    return make_response(jsonify({'error': 'Missing json parameter'}), 404)

  sku = {
    "sku": request.json['sku'],
    "price_balance": request.json['price_balance']
  }

  priceBalancerManager = PriceBalancerManager()
  result = priceBalancerManager.insertPriceBalancer(sku, request.args.get('token'))
  if 'success' in result:
    return make_response(jsonify(result), 201)
  else:
    return make_response(jsonify(result), 404)

# ------------------------------------------------------------------------------
# Delete a price balancer
# ------------------------------------------------------------------------------
@SkuAPI.route('/price-balancer/delete', methods=['POST'])
@cross_origin()
def deletePriceBalancer():
  if not request.args:
    return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
  if not 'token' in request.args:
    return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
  if not 'id' in request.json:
    return make_response(jsonify({'error': 'Missing json parameter'}), 404)

  sku = {"id": request.json['id']}

  priceBalancerManager = PriceBalancerManager()
  result = priceBalancerManager.deletePriceBalancer(sku, request.args.get('token'))
  if 'success' in result:
    return make_response(jsonify(result), 201)
  else:
    return make_response(jsonify(result), 404)

# ------------------------------------------------------------------------------
# Update a price balancer
# ------------------------------------------------------------------------------
@SkuAPI.route('/price-balancer/update', methods=['GET'])
@cross_origin()
def updatePriceBalancer():
  if not request.args:
    return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
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

  priceBalancerManager = PriceBalancerManager()
  result = priceBalancerManager.updatePriceBalancer(sku, request.args.get('token'))
  if 'success' in result:
    return make_response(jsonify(result), 201)
  else:
    return make_response(jsonify(result), 404)

# ------------------------------------------------------------------------------
# Get all skus of price balancer
# ------------------------------------------------------------------------------
@SkuAPI.route('/price-balancer/get-all', methods=['GET'])
@cross_origin()
def getAllSkuOfPriceBalancer():
  if not request.args:
    return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
  if not 'token' in request.args:
    return make_response(jsonify({'error': 'Missing token parameter value'}), 404)

  priceBalancerManager = PriceBalancerManager()
  result = priceBalancerManager.getAll(request.args.get('token'))
  if 'success' in result:
    return make_response(jsonify(result), 201)
  else:
    return make_response(jsonify(result), 404)












