import time
import simplejson as json
from flask_cors import CORS, cross_origin
from flask import Blueprint, render_template, abort, request, make_response, jsonify
from controllers.accountstatement.account_statement_controller import AccountStatementController


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

	accountStatmentCtr = AccountStatementController()
	data = accountStatmentCtr.getAllAccountStatement(token)
	if 'error' in data != None:
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
	print("account statement id: {} ".format(accountStatementId))

	accountStatmentCtr = AccountStatementController()
	data = accountStatmentCtr.getAccountStatementInfo(token, accountStatementId)
	if 'error' in data != None:
		return make_response(jsonify(data), 404)
	else:
		return make_response(jsonify(data), 201)

# @AccountStatementAPI.route('/account-statement/update-account-statement-price', methods=['POST'])
# @cross_origin()
# def updateAccountStatement():
# 	if not request.args:
# 		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
# 	if not request.json:
# 		return make_response(jsonify({'error': 'Missing json parameters value'}), 404)
# 	if not 'id' in request.json:
# 		return make_response(jsonify({'error': 'Missing id parameter'}), 404)
# 	if not 'price' in request.json:
# 		return make_response(jsonify({'error': 'Missing price parameter'}), 404)
# 	if not 'shop_sku' in request.json:
# 		return make_response(jsonify({'error': 'Missing id parameter'}), 404)
# 	if not 'excel_url' in request.json:
# 		return make_response(jsonify({'error': 'Missing price parameter'}), 404)

# 	accountStatement = {
# 		"id": request.json['id'],
# 		"price": request.json['price'],
# 		"shop_sku": request.json['shop_sku'],
# 		"excel_url": request.json['excel_url']
# 	}

# 	# Update original_price of product if it's 0
# 	# Re-calculate item earned

# 	accountStatementDao = AccountStatementDao()
# 	result, exception = accountStatementDao.updateAccountStatement(accountStatement)

# 	if 'success' in result:
# 		return make_response(jsonify({"success": "done"}))
# 	else:
# 		return make_response(jsonify(result))



