import time
from flask_cors import CORS, cross_origin
from flask import Blueprint, render_template, abort, request, make_response, jsonify


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
		"min_price": request.json['min_price'],
		"max_price": request.json['max_price'],
		"subtract_price": request.json['subtract_price'],
		"state": request.json['state'],
		"repeat_time": request.json['repeat_time'],
		"created_at": int(round(time.time())),
		"updated_at": 0
	}

	return make_response(jsonify(sku), 201)




