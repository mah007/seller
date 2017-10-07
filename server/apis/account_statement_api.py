import time
import simplejson as json
from flask_cors import CORS, cross_origin
from flask import Blueprint, render_template, abort, request, make_response, jsonify
from controllers.finance.account_statement_controller import AccountStatementController


AccountStatementAPI = Blueprint('account_statement_api', __name__, template_folder='apis')

# ------------------------------------------------------------------------------
# Get all account statement
# ------------------------------------------------------------------------------
@AccountStatementAPI.route('/account-statement/get-all', methods=['GET'])
@cross_origin()
def getAllAccountStatement():
	if (not request.args):
		return make_response(jsonify({'error': 'Missing token parameter'}), 404)
	if (not 'token' in request.args):
		return make_response(jsonify({'error': 'Missing token parameter'}), 404)
	token = request.args.get('token')
	if token == None or token == "":
		return make_response(jsonify({'error': 'Missing token parameter'}), 404)

	accountStatmentCtrl = AccountStatementController()
	data = accountStatmentCtrl.getAllAccountStatement(token)
	if 'error' in data:
		return make_response(jsonify(data), 404)
	else:
		return make_response(jsonify(data), 201)

# ------------------------------------------------------------------------------
# Get all account statement exception
# ------------------------------------------------------------------------------
@AccountStatementAPI.route('/account-statement/get-info', methods=['POST'])
@cross_origin()
def getAccountStatementInfo():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not 'token' in request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	token = request.args.get('token')
	if token == None or token == "":
		return make_response(jsonify({'error': 'Missing token parameter'}), 404)
	if not 'account_statement_id' in request.json:
		return make_response(jsonify({'error': 'Missing json parameter value'}), 404)

	accountStatementId = request.json['account_statement_id']
	accountStatmentCtrl = AccountStatementController()
	data = accountStatmentCtrl.getAccountStatementInfo(token, accountStatementId)
	if 'error' in data:
		return make_response(jsonify(data), 404)
	else:
		return make_response(jsonify(data), 201)

@AccountStatementAPI.route('/account-statement/update-original-prices', methods=['POST'])
@cross_origin()
def updateAccountStatement():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not 'token' in request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	token = request.args.get('token')
	if token == None or token == "":
		return make_response(jsonify({'error': 'Missing token parameter'}), 404)
	if not request.json:
		return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
	if not 'order_items' in request.json:
		return make_response(jsonify({'error': 'Missing Order Items parameter'}), 404)
	if not 'account_statement_id' in request.json:
		return make_response(jsonify({'error': 'Missing account statement id parameter'}), 404)

	orderItems = request.json['order_items']
	accountStatementId = request.json['account_statement_id']
	accountStatmentCtrl = AccountStatementController()
	result = accountStatmentCtrl.changeOriginPrice(token, orderItems, accountStatementId)
	if 'error' in result:
		return make_response(jsonify(result), 404)
	else:
		return make_response(jsonify(result), 201)



