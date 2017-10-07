import simplejson as json
from flask_cors import CORS, cross_origin
from flask import Blueprint, render_template, abort, request, make_response, jsonify
from controllers.product.product_controller import ProductController
from lazada_api.lazada_order_api import LazadaOrderApi
from utils.timestamp_utils import TimestampUtils
from utils.string_utils import StringUtils


ProductAPI = Blueprint('product_api', __name__, template_folder='apis')

# ------------------------------------------------------------------------------
# Get Product
# TODO: add pagination
# ------------------------------------------------------------------------------
@ProductAPI.route('/product/get-products', methods=['GET'])
@cross_origin()
def getAllProduct():
	if (not request.args):
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if (not 'token' in request.args):
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	token = request.args.get('token')
	if (StringUtils.isEmpty(token)):
		return make_response(jsonify({'error': 'Missing token parameter'}), 404)

	productCtrl = ProductController()
	result = productCtrl.getProducts(request.args.get('token'))
	if 'success' in result:
		return make_response(jsonify(result), 201)
	else:
		return make_response(jsonify(result), 404)

# ------------------------------------------------------------------------------
# Update Product quantity and original price
# ------------------------------------------------------------------------------
@ProductAPI.route('/product/update-quantity-and-orginal-price', methods=['POST'])
@cross_origin()
def updateQuantityAndOriginalPrice():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not 'token' in request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	token = request.args.get('token')
	if (StringUtils.isEmpty(token)):
		return make_response(jsonify({'error': 'Missing token parameter'}), 404)
	if not request.json:
		return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
	if not 'products' in request.json:
		return make_response(jsonify({'error': 'Missing json parameter'}), 404)

	products = request.json['products']
	productCtrl = ProductController()
	result = productCtrl.updateProductQuantityAndOriginalPrice(token, products)
	if 'success' in result:
		return make_response(jsonify(result), 201)
	else:
		return make_response(jsonify(result), 404)

# ------------------------------------------------------------------------------
# Search Product by name, seller sku, shop sku, brand and model
# ------------------------------------------------------------------------------
@ProductAPI.route('/product/search', methods=['POST'])
@cross_origin()
def searchProduct():
  if not request.args:
  	return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
  if not 'token' in request.args:
  	return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
  token = request.args.get('token')
  if (StringUtils.isEmpty(token)):
  	return make_response(jsonify({'error': 'Missing token parameter'}), 404)
  if not request.json:
    return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
  if not 'search_key' in request.json:
    return make_response(jsonify({'error': 'Missing json parameter'}), 404)

  searchKey = request.json['search_key']
  productCtrl = ProductController()
  result = productCtrl.searchProduct(token, searchKey)
  if 'success' in result:
    return make_response(jsonify(result), 201)
  else:
    return make_response(jsonify(result), 404)

# ------------------------------------------------------------------------------
# Search Product by name, seller sku, shop sku, brand and model
# ------------------------------------------------------------------------------
@ProductAPI.route('/product/top-selling-products', methods=['GET'])
@cross_origin()
def getTopSellingProducts():
  if not request.args:
  	return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
  if not 'token' in request.args:
  	return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
  token = request.args.get('token')
  if (StringUtils.isEmpty(token)):
  	return make_response(jsonify({'error': 'Missing token parameter'}), 404)

  productCtrl = ProductController()
  result = productCtrl.getTopSellingProducts(token)
  if 'success' in result:
    return make_response(jsonify(result), 201)
  else:
    return make_response(jsonify(result), 404)













