import time
import simplejson as json
from flask_cors import CORS, cross_origin
from flask import Blueprint, render_template, abort, request, make_response, jsonify
from managers.sku_manager import SkuManager


SkuAPI = Blueprint('sku_api', __name__, template_folder='apis')


# ------------------------------------------------------------------------------
# Get All KSU
# ------------------------------------------------------------------------------
@SkuAPI.route('/sku/get-all', methods=['GET'])
@cross_origin()
def getAll():
	if not request.args:
		return make_response(jsonify({'error': 'Missig token parameter value'}), 404)

	token = request.args.get('token')
	skuManager = SkuManager()
	result = skuManager.getAll(token)
	if 'error' in result:
		return make_response(jsonify(result))
	else:
		return make_response(jsonify({"data": result}))


# ------------------------------------------------------------------------------
# Delete KSU
# ------------------------------------------------------------------------------
@SkuAPI.route('/sku/delete', methods=['POST'])
@cross_origin()
def delete():
	if not request.args:
		return make_response(jsonify({'error': 'Missig token parameter value'}), 404)
	if not request.json:
		return make_response(jsonify({'error': 'Missig json parameters value'}), 404)
	if not 'id' in request.json:
		return make_response(jsonify({'error': 'Missig json parameter'}), 404)

	sku = {
		"id": request.json['id']
	}

	skuManager = SkuManager()
	result = skuManager.deleteSku(sku, request.args.get('token'))
	if 'success' in result:
		return make_response(jsonify({"success": "done"}))
	else:
		return make_response(jsonify(result))

# ------------------------------------------------------------------------------
# Update SKU's state
# ------------------------------------------------------------------------------
@SkuAPI.route('/sku/update-state', methods=['POST'])
@cross_origin()
def updateSkuState():
	if not request.args:
		return make_response(jsonify({'error': 'Missig token parameter value'}), 404)
	if not request.json:
		return make_response(jsonify({'error': 'Missig json parameters value'}), 404)
	if not 'id' in request.json:
		return make_response(jsonify({'error': 'Missig json parameter'}), 404)
	if not 'state' in request.json:
		return make_response(jsonify({'error': 'Missig state parameter'}), 404)

	sku = {
		"id": request.json['id'],
		"state": request.json['state']
	}

	skuManager = SkuManager()
	result = skuManager.updateSkuState(sku, request.args.get('token'))
	if 'success' in result:
		return make_response(jsonify({"success": "done"}))
	else:
		return make_response(jsonify(result))


# ------------------------------------------------------------------------------
# Insert KSU
# ------------------------------------------------------------------------------
@SkuAPI.route('/sku/insert', methods=['POST'])
@cross_origin()
def insert():
	if not request.args:
		return make_response(jsonify({'error': 'Missig token parameter value'}), 404)
	if not request.json:
		return make_response(jsonify({'error': 'Missig json parameters value'}), 404)
	if not 'sku' in request.json:
		return make_response(jsonify({'error': 'Missig sku parameter'}), 404)
	if not 'min_price' in request.json:
		return make_response(jsonify({'error': 'Missig min_price parameter'}), 404)
	if not 'max_price' in request.json:
		return make_response(jsonify({'error': 'Missig max_price parameter'}), 404)
	if not 'compete_price' in request.json:
		return make_response(jsonify({'error': 'Missig compete_price parameter'}), 404)
	if not 'state' in request.json:
		return make_response(jsonify({'error': 'Missig state parameter'}), 404)
	if not 'repeat_time' in request.json:
		return make_response(jsonify({'error': 'Missig repeat_time parameter'}), 404)

	sku = {
		"sku": request.json['sku'],
		"name": "null",
		"link": "null",
		"min_price": int(request.json['min_price']),
		"max_price": int(request.json['max_price']),
		"compete_price": int(request.json['compete_price']),
		"special_price": 0,
		"state": int(request.json['state']),
		"repeat_time": int(request.json['repeat_time']),
		"created_at": int(round(time.time()))
	}

	skuManager = SkuManager()
	result = skuManager.insertSku(sku, request.args.get('token'))
	if 'success' in result:
		return make_response(json.dumps(sku), 201)
	else:
		return make_response(jsonify(result), 404)


# ---------------------------------------------------------------------------------------
# Update KSU
# ---------------------------------------------------------------------------------------
@SkuAPI.route('/sku/update', methods=['POST'])
@cross_origin()
def update():
	if not request.json:
		return make_response(jsonify({'error': 'Missig json parameters value'}), 404)
	if not 'id' in request.json:
		return make_response(jsonify({'error': 'Missig id parameter'}), 404)
	if not 'sku' in request.json:
		return make_response(jsonify({'error': 'Missig sku parameter'}), 404)
	if not 'min_price' in request.json:
		return make_response(jsonify({'error': 'Missig min_price parameter'}), 404)
	if not 'max_price' in request.json:
		return make_response(jsonify({'error': 'Missig max_price parameter'}), 404)
	if not 'compete_price' in request.json:
		return make_response(jsonify({'error': 'Missig compete_price parameter'}), 404)
	if not 'state' in request.json:
		return make_response(jsonify({'error': 'Missig state parameter'}), 404)
	if not 'repeat_time' in request.json:
		return make_response(jsonify({'error': 'Missig repeat_time parameter'}), 404)

	sku = {
		"id": request.json['id'],
		"min_price": int(request.json['min_price']),
		"max_price": int(request.json['max_price']),
		"compete_price": int(request.json['compete_price']),
		"state": int(request.json['state']),
		"repeat_time": int(request.json['repeat_time']),
		"updated_at": int(round(time.time()))
	}

	skuManager = SkuManager()
	result = skuManager.updateSku(sku, request.args.get('token'))
	if 'success' in result:
		return make_response(jsonify(sku), 201)
	else:
		return make_response(jsonify(result), 404)








