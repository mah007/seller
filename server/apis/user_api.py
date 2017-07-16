import time
import simplejson as json
from flask_cors import CORS, cross_origin
from flask import Blueprint, render_template, abort, request, make_response, jsonify
from managers.sku_manager import SkuManager
from managers.user_manager import UserManager
from lazada_api.lazada_sku_api import LazadaSkuApi


UserAPI = Blueprint('user_api', __name__, template_folder='apis')

# ------------------------------------------------------------------------------
# Login
# ------------------------------------------------------------------------------
@UserAPI.route('/user/login', methods=['POST'])
@cross_origin()
def login():
	if not 'username' in request.json:
		return make_response(jsonify({'error': 'Missig username parameter'}), 404)
	if not 'password' in request.json:
		return make_response(jsonify({'error': 'Missig password parameter'}), 404)

	username = request.json['username']
	password = request.json['password']
	user = {
		"username": username,
		"password": password
	}

	userManager = UserManager()
	result = userManager.login(user);
	if 'success' in result:
		return make_response(jsonify(result))
	else:
		return make_response(jsonify(result), 403)


# ------------------------------------------------------------------------------
# Get All User
# ------------------------------------------------------------------------------
@UserAPI.route('/user/get-all', methods=['GET'])
@cross_origin()
def getAll():
	# if not request.args:
	# 	return make_response(jsonify({'error': 'Missig token parameter value'}), 404)

	# token = request.args.get('token')
	userManager = UserManager()
	result = userManager.getAll()
	if 'error' in result:
		return make_response(jsonify(result))
	else:
		return make_response(jsonify({"data": result}))


# ------------------------------------------------------------------------------
# User KSU
# ------------------------------------------------------------------------------
@UserAPI.route('/user/delete', methods=['POST'])
@cross_origin()
def delete():
	# if not request.args:
	# 	return make_response(jsonify({'error': 'Missig token parameter value'}), 404)
	# if not request.json:
	# 	return make_response(jsonify({'error': 'Missig json parameters value'}), 404)
	if not 'id' in request.json:
		return make_response(jsonify({'error': 'Missig json parameter'}), 404)

	user = {
		"id": request.json['id']
	}

	userManager = UserManager()
	result = userManager.deleteUser(user)
	return make_response(jsonify({"success": "done"}))
	# if 'success' in result:
	# 	return make_response(jsonify({"success": "done"}))
	# else:
	# 	return make_response(jsonify(result))


# ---------------------------------------------------------------------------------------
# Update USER
# ---------------------------------------------------------------------------------------
@UserAPI.route('/user/update', methods=['POST'])
@cross_origin()
def update():
	if not request.json:
		return make_response(jsonify({'error': 'Missig json parameters value'}), 404)
	if not 'id' in request.json:
		return make_response(jsonify({'error': 'Missig id parameter'}), 404)
	if not 'password' in request.json:
		return make_response(jsonify({'error': 'Missig password parameter'}), 404)

	user = {
		"id": request.json['id'],
		"username": (request.json['username']),
		"password": (request.json['password']),
		"lazada_username": (request.json['lazada_username']),
		"lazada_userid": (request.json['lazada_userid']),
		"lazada_apikey": (request.json['lazada_apikey'])
	}

	userManage = UserManager()
	result = userManage.updateUser(user)
	return make_response(jsonify({"success": "done"}))
	# if 'success' in result:
	# 	return make_response(jsonify(user), 201)
	# else:
	# 	return make_response(jsonify(result), 404)


# ------------------------------------------------------------------------------
# Insert User
# ------------------------------------------------------------------------------
@UserAPI.route('/user/insert', methods=['POST'])
@cross_origin()
def insert():
	if not 'username' in request.json:
		return make_response(jsonify({'error': 'Missig username parameter'}), 404)
	if not 'password' in request.json:
		return make_response(jsonify({'error': 'Missig password parameter'}), 404)
	if not 'lazada_user_name' in request.json:
		return make_response(jsonify({'error': 'Missig lazada_username parameter'}), 404)
	if not 'lazada_user_id' in request.json:
		return make_response(jsonify({'error': 'Missig lazada_userid parameter'}), 404)
	if not 'lazada_api_key' in request.json:
		return make_response(jsonify({'error': 'Missig lazada_apikey parameter'}), 404)

	user = {
		"username": request.json['username'],
		"password": request.json['password'],
		"lazada_user_name": request.json['lazada_user_name'],
		"lazada_user_id": request.json['lazada_user_id'],
		"lazada_api_key": request.json['lazada_api_key'],
		"created_at": int(round(time.time()))
	}

	userManager = UserManager()
	result = userManager.insertUser(user)
	if 'success' in result:
		return make_response(json.dumps(user), 201)
	else:
		return make_response(jsonify(result), 404)







