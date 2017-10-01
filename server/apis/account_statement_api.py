import time
import simplejson as json
from flask_cors import CORS, cross_origin
from flask import Blueprint, render_template, abort, request, make_response, jsonify
from managers.account_statement_manager import AccountStatementManager


AccountStatementAPI = Blueprint('account_statement_api', __name__, template_folder='apis')

# ------------------------------------------------------------------------------
# Get all account statement
# ------------------------------------------------------------------------------
@AccountStatementAPI.route('/account-statement/get-all-account-statement', methods=['GET'])
@cross_origin()
def getAllAccountStatement():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not 'token' in request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)

	print("Start")
	accountStatementManager = AccountStatementManager()
	result = accountStatementManager.getAllAccountStatement(request.args.get('token'))
	print(result)
	if 'success' in result:
		return make_response(jsonify(result), 201)
	else:
		return make_response(jsonify(result), 404)

# ------------------------------------------------------------------------------
# Get all account statement exception
# ------------------------------------------------------------------------------
@AccountStatementAPI.route('/account-statement/get-all-account-statement-exception', methods=['GET'])
@cross_origin()
def getAllAccountStatementException():
	if not request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)
	if not 'token' in request.args:
		return make_response(jsonify({'error': 'Missing token parameter value'}), 404)

	accountStatementManager = AccountStatementManager()
	result = accountStatementManager.getAllAccountStatementException(request.args.get('token'))
	if 'success' in result:
		return make_response(jsonify(result), 201)
	else:
		return make_response(jsonify(result), 404)



