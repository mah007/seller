import time
from flask_cors import CORS, cross_origin
from flask import Blueprint, render_template, abort, request, make_response, jsonify
from managers.sku_manager import SkuManager
from managers.user_manager import UserManager
from lazada_api.lazada_sku_api import LazadaSkuApi


SkuAPI = Blueprint('sku_api', __name__, template_folder='apis')

@SkuAPI.route('/sku/insert', methods=['POST'])
@cross_origin()
def insert():
	print request.data
	if not request.json:
		return make_response(jsonify({'error': 'Missig json parameters value'}), 404)
	if not 'sku' in request.json:
		return make_response(jsonify({'error': 'Missig sku parameter'}), 404)		
	if not 'min_price' in request.json:
		return make_response(jsonify({'error': 'Missig min_price parameter'}), 404)
	if not 'max_price' in request.json:
		return make_response(jsonify({'error': 'Missig max_price parameter'}), 404)
	if not 'subtract_price' in request.json:
		return make_response(jsonify({'error': 'Missig subtract_price parameter'}), 404)
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
		"subtract_price": int(request.json['subtract_price']),
		"state": int(request.json['state']),
		"repeat_time": int(request.json['repeat_time']),
		"created_at": int(round(time.time()))
	}

	userManager = UserManager()
	temporaryUser = userManager.getUser("token");

	lazadaSkuApi = LazadaSkuApi()
	lazadaProduct = lazadaSkuApi.getSku(sku, temporaryUser)
	
	if (lazadaProduct):
		sku['name'] = lazadaProduct['Attributes']['name'].encode('utf-8')
		sku['link'] = lazadaProduct['Skus'][0]['Url'].encode('utf-8')
		skuManager = SkuManager()
		skuManager.insertSku(sku)
		return make_response(jsonify(sku), 201)
	else:
		return make_response(jsonify({'error': 'Cant find sku from your products on lazada'}), 404)












