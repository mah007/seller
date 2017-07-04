import simplejson as json
from flask_cors import CORS, cross_origin
from flask import Blueprint, render_template, abort, request, make_response, jsonify
from managers.sku_manager import SkuManager
from managers.user_manager import UserManager
from lazada_api.lazada_sku_api import LazadaSkuApi


UserAPI = Blueprint('user_api', __name__, template_folder='apis')

# ---------------------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------------------
@UserAPI.route('/user/login', methods=['POST'])
@cross_origin()
def login():
	# if not request.json:
		# return make_response(jsonify({'error': 'Missig json parameters value'}), 404)
	if not 'username' in request.json:
		return make_response(jsonify({'error': 'Missig username parameter'}), 404)
	if not 'password' in request.json:
		return make_response(jsonify({'error': 'Missig password parameter'}), 404)

	login = {
		"username": request.json['username'],
		"password": request.json['password']
	}

	# skuManager = SkuManager()
	# if(skuManager.login(sku)):
	# 	return make_response(jsonify({"success": "done"}))	
	# else:
	# 	return make_response(jsonify({'error': 'Incorrect Account'}), 404)
	userManager = UserManager()
	if(userManager.login(login) == 1):
		return make_response(jsonify({"success": "done"}))
	else:
		return make_response(jsonify({'error': 'Incorres Account'}), 404)