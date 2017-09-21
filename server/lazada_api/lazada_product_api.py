import requests
import json
from config import LazadaAPI
from lazada_api.lazada_api_helper import LazadaApiHelper
from utils.exception_utils import ExceptionUtils



class LazadaProductApi(object):

	#-----------------------------------------------------------------------------
	# Get Produts from Lazada
	#-----------------------------------------------------------------------------
	def getProducts(self, user, timestamp):
		parameters = {
		'Action': 'GetProducts',
		'Format':'JSON',
		'Timestamp': LazadaApiHelper.getCurrentUTCTime(),
		'UserID': user['lazada_user_id'],
		'Version': '1.0',
		'CreatedBefore': LazadaApiHelper.getCurrentUTCTime(),
		'Filter': 'all',
		'Limit': LazadaAPI.LIMIT,
		'Offset': constant
		}

		parameters['Signature'] = LazadaApiHelper.generateSignature(parameters, user['lazada_api_key'])
		url = "{}/?Action={}&Format={}&Timestamp={}&UserID={}&Version={}&Signature={}&CreatedBefore={}&Filter={}&Offset={}&Limit={}".format(
						LazadaAPI.ENDPOINT,
		 				parameters["Action"],
		 				parameters["Format"],
		 				LazadaApiHelper.formatTimestamp(parameters["Timestamp"]),
		 				parameters["UserID"],
		 				parameters["Version"],
		 				parameters["Signature"],
		 				LazadaApiHelper.formatTimestamp(parameters["CreatedBefore"]),
		 				parameters["Filter"],
		 				parameters["Offset"],
		 				parameters["Limit"])
		try:
			resp = requests.get(url)
			if resp.status_code == 200:
				response = json.loads(resp.text)
				if ('ErrorResponse' in response):
					return ExceptionUtils.returnError('''Get Products is error: ''', response)

				data = response['SuccessResponse']['Body']
				return data['Products'], data['TotalProducts']

			return ExceptionUtils.error('''Get Products is error: {}'''.format(resp.status_code))
		except Exception as ex:
			return ExceptionUtils.error('''Get Products is error: {}'''.format(str(ex)))

	#-----------------------------------------------------------------------------
	# Get Produts by CreatedAfter
	#-----------------------------------------------------------------------------
	def getProductsWithCreatedAfter(self, user, constant):
		parameters = {
		'Action': 'GetProducts',
		'Format':'JSON',
		'Timestamp': LazadaApiHelper.getCurrentUTCTime(),
		'UserID': user['lazada_user_id'],
		'Version': '1.0',
		'CreatedAfter': LazadaApiHelper.getCurrentUTCTime(),
		'Filter': 'all',
		'Limit': LazadaAPI.LIMIT
		}

		parameters['Signature'] = LazadaApiHelper.generateSignature(parameters, user['lazada_api_key'])
		url = "{}/?Action={}&Format={}&Timestamp={}&UserID={}&Version={}&Signature={}&CreatedBefore={}&Filter={}&Offset={}&Limit={}".format(
						LazadaAPI.ENDPOINT,
		 				parameters["Action"],
		 				parameters["Format"],
		 				LazadaApiHelper.formatTimestamp(parameters["Timestamp"]),
		 				parameters["UserID"],
		 				parameters["Version"],
		 				parameters["Signature"],
		 				LazadaApiHelper.formatTimestamp(parameters["CreatedAfter"]),
		 				parameters["Filter"],
		 				parameters["Limit"])
		try:
			resp = requests.get(url)
			if resp.status_code == 200:
				response = json.loads(resp.text)
				if ('ErrorResponse' in response):
					return ExceptionUtils.returnError('''Get Products is error: ''', response)

				data = response['SuccessResponse']['Body']
				return data['Products'], data['TotalProducts']

			return ExceptionUtils.error('''Get Products is error: {}'''.format(resp.status_code))
		except Exception as ex:
			return ExceptionUtils.error('''Get Products is error: {}'''.format(str(ex)))



