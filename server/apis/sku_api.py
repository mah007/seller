import time
import simplejson as json
from flask_cors import CORS, cross_origin
from flask import Blueprint, render_template, abort, request, make_response, jsonify
from managers.sku_manager import SkuManager
from managers.product_manager import ProductManager

SkuAPI = Blueprint('sku_api', __name__, template_folder='apis')

# ------------------------------------------------------------------------------
# Get Sku histories
# ------------------------------------------------------------------------------
@SkuAPI.route('/sku/get-all-history', methods=['GET'])
@cross_origin()
def getAllHistory():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not 'token' in request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)

	skuManager = SkuManager()
	result = skuManager.getAllHistory(request.args.get('token'))
	if 'success' in result:
		return make_response(jsonify(result), 201)
	else:
		return make_response(jsonify(result), 404)

# ------------------------------------------------------------------------------
# Get All SKU
# ------------------------------------------------------------------------------
@SkuAPI.route('/sku/get-all', methods=['GET'])
@cross_origin()
def getAll():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not 'token' in request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)

	skuManager = SkuManager()
	result = skuManager.getAll(request.args.get('token'))
	if 'success' in result:
		return make_response(jsonify(result), 201)
	else:
		return make_response(jsonify(result), 404)


# ------------------------------------------------------------------------------
# Delete SKU
# ------------------------------------------------------------------------------
@SkuAPI.route('/sku/delete', methods=['POST'])
@cross_origin()
def delete():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not request.json:
		return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
	if not 'id' in request.json:
		return make_response(jsonify({'error': 'Missing json parameter'}), 404)

	sku = {
		"id": request.json['id']
	}

	skuManager = SkuManager()
	result = skuManager.deleteSku(sku, request.args.get('token'))
	if 'success' in result:
		return make_response(jsonify({"success": "done"}), 201)
	else:
		return make_response(jsonify(result), 404)

# ------------------------------------------------------------------------------
# Update SKU's state
# ------------------------------------------------------------------------------
@SkuAPI.route('/sku/update-state', methods=['POST'])
@cross_origin()
def updateSkuState():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not request.json:
		return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
	if not 'id' in request.json:
		return make_response(jsonify({'error': 'Missing json parameter'}), 404)
	if not 'state' in request.json:
		return make_response(jsonify({'error': 'Missing state parameter'}), 404)

	sku = {
		"id": request.json['id'],
		"state": request.json['state']
	}

	skuManager = SkuManager()
	result = skuManager.updateSkuState(sku, request.args.get('token'))
	if 'success' in result:
		return make_response(jsonify({"success": "done"}), 201)
	else:
		return make_response(jsonify(result), 404)


# ------------------------------------------------------------------------------
# Insert SKU
# ------------------------------------------------------------------------------
@SkuAPI.route('/sku/insert', methods=['POST'])
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
	if not 'min_price' in request.json:
		return make_response(jsonify({'error': 'Missing min_price parameter'}), 404)
	if not 'max_price' in request.json:
		return make_response(jsonify({'error': 'Missing max_price parameter'}), 404)
	if not 'compete_price' in request.json:
		return make_response(jsonify({'error': 'Missing compete_price parameter'}), 404)
	if not 'state' in request.json:
		return make_response(jsonify({'error': 'Missing state parameter'}), 404)

	sku = {
		"sku": request.json['sku'],
		"name": "null",
		"link": "null",
		"min_price": int(request.json['min_price']),
		"max_price": int(request.json['max_price']),
		"compete_price": int(request.json['compete_price']),
		"special_price": 0,
		"state": int(request.json['state']),
		"created_at": int(round(time.time()))
	}

	skuManager = SkuManager()
	result = skuManager.insertSku(sku, request.args.get('token'))
	if 'success' in result:
		return make_response(json.dumps(sku), 201)
	else:
		return make_response(jsonify(result), 404)


# ---------------------------------------------------------------------------------------
# Update SKU
# ---------------------------------------------------------------------------------------
@SkuAPI.route('/sku/update', methods=['POST'])
@cross_origin()
def update():
	if not request.json:
		return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
	if not 'id' in request.json:
		return make_response(jsonify({'error': 'Missing id parameter'}), 404)
	if not 'sku' in request.json:
		return make_response(jsonify({'error': 'Missing sku parameter'}), 404)
	if not 'min_price' in request.json:
		return make_response(jsonify({'error': 'Missing min_price parameter'}), 404)
	if not 'max_price' in request.json:
		return make_response(jsonify({'error': 'Missing max_price parameter'}), 404)
	if not 'compete_price' in request.json:
		return make_response(jsonify({'error': 'Missing compete_price parameter'}), 404)
	if not 'state' in request.json:
		return make_response(jsonify({'error': 'Missing state parameter'}), 404)

	sku = {
		"id": request.json['id'],
		"min_price": int(request.json['min_price']),
		"max_price": int(request.json['max_price']),
		"compete_price": int(request.json['compete_price']),
		"state": int(request.json['state']),
		"updated_at": int(round(time.time()))
	}

	skuManager = SkuManager()
	result = skuManager.updateSku(sku, request.args.get('token'))
	if 'success' in result:
		return make_response(jsonify(sku), 201)
	else:
		return make_response(jsonify(result), 404)

# ------------------------------------------------------------------------------
# Search sku by seller sku
# ------------------------------------------------------------------------------
@SkuAPI.route('/sku/search', methods=['POST'])
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
  productManager = ProductManager()
  result = productManager.searchProduct(token, searchKey)
  if 'success' in result:
    return make_response(jsonify(result), 201)
  else:
    return make_response(jsonify(result), 404)



