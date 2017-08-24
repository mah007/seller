import time
import simplejson as json
from flask_cors import CORS, cross_origin
from flask import Blueprint, render_template, abort, request, make_response, jsonify
from managers.enemy_manager import EnemyManager
from lazada_api.lazada_order_api import LazadaOrderApi


EnemyAPI = Blueprint('enemy_api', __name__, template_folder='apis')


# ------------------------------------------------------------------------------
# Get All SKU
# ------------------------------------------------------------------------------
@EnemyAPI.route('/enemy/get-all', methods=['GET'])
@cross_origin()
def getAll():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not 'token' in request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)

	user = {
		"id": 1
	}

	enemyManager = EnemyManager()
	result = enemyManager.getEnemy(user, request.args.get('token'))
	if 'success' in result:
		return make_response(jsonify(result))
	else:
		return make_response(jsonify(result), 404)

