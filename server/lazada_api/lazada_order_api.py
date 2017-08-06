import requests
import json
from lazada_api.lazada_api_helper import LazadaApiHelper
from config import LazadaAPI
from utils.exception_utils import ExceptionUtils



# Todo:
# 1. Get error from error response util.

class LazadaOrderApi(object):

	#-----------------------------------------------------------------------------
	# Refresh all orders
	#-----------------------------------------------------------------------------
	def refreshAllOrder(self, user):
		parameters = {
		'Action': 'GetOrders',
		'Format':'JSON',
		'Timestamp': LazadaApiHelper.getCurrentUTCTime(),
		'UserID': user['lazada_user_id'],
		'Version': '1.0',
		'CreatedBefore': LazadaApiHelper.getCurrentUTCTime(),
		'Status': 'pending'
		}

		parameters['Signature'] = LazadaApiHelper.generateSignature(parameters, user['lazada_api_key'])
		url = "{}?Action={}&CreatedBefore={}&Format={}&Status={}&Timestamp={}&UserID={}&Version={}&Signature={}".format(
						LazadaAPI.ENDPOINT,
		 				parameters["Action"],
		 				LazadaApiHelper.formatTimestamp(parameters["CreatedBefore"]),
		 				parameters["Format"],
		 				parameters["Status"],
		 				LazadaApiHelper.formatTimestamp(parameters["Timestamp"]),
		 				parameters["UserID"],
		 				parameters["Version"],
		 				parameters["Signature"])

		try:
			resp = requests.get(url)
			if resp.status_code == 200:
				response = json.loads(resp.text)
				if ('ErrorResponse' in response):
					return ExceptionUtils.error('''User: {}-{}, Get Orders is error: {}'''.format(user['id'], user['username'], esponse['ErrorResponse']['Head']['ErrorMessage']))

				data = response['SuccessResponse']['Body']
				if (data['Orders'] != None):
					return data['Orders']

			return ExceptionUtils.error('''User: {}-{}, Get Orders is error: {}'''.format(user['id'], user['username'], resp.status_code))
		except Exception as ex:
			return ExceptionUtils.error('''User: {}-{}, Get Orders is error: {}'''.format(user['id'], user['username'], str(ex)))


	#-----------------------------------------------------------------------------
	# Get order item by order id
	#
	# Need refactor: separate logic and request
	#-----------------------------------------------------------------------------
	def getOrderItems(self, order, user):
		parameters = {
		'Action': 'GetOrderItems',
		'Format':'json',
		'Timestamp': LazadaApiHelper.getCurrentUTCTime(),
		'UserID': user['lazada_user_id'],
		'Version': '1.0',
		'OrderId': str(order['OrderId'])
		}

		parameters['Signature'] = LazadaApiHelper.generateSignature(parameters, user['lazada_api_key'])
		url = "{}?Action={}&Format={}&OrderId={}&Timestamp={}&UserID={}&Version={}&Signature={}".format(
						LazadaAPI.ENDPOINT,
		 				parameters["Action"],
		 				parameters["Format"],
		 				parameters['OrderId'],
		 				LazadaApiHelper.formatTimestamp(parameters["Timestamp"]),
		 				parameters["UserID"],
		 				parameters["Version"],
		 				parameters["Signature"])

		try:
			resp = requests.get(url)
			if resp.status_code == 200:
				response = json.loads(resp.text)
				# Lazada return exception
				if 'ErrorResponse' in response:
					return ExceptionUtils.error('''User: {}-{}, Get OrderItem: {} is error: {}'''.format(user['id'], user['username'], order['OrderNumber'], response['ErrorResponse']['Head']['ErrorMessage']))

				data = response['SuccessResponse']['Body']
				result = data['OrderItems']
				length = len(result)
				finalResult = []
				count = 1

				if (result != None and length >= 2):
					for i in range(0, length - 1):
						for j in range(1, length ):
							if(result[i]['TrackingCode'] == result[j]['TrackingCode']):
								count = count + 1
								result.remove(result[j])

						result[i]['Count'] = count
						finalResult.append(result[i])
						print(count)
						count = 1

				if (result != None and length == 1):
					result[0]['Count'] = 1
					finalResult.append(result[0])
					count = 1

				return finalResult # Success with result

			# Request except
			return ExceptionUtils.error('''User: {}-{}, Get OrderItem: {} is error: {}'''.format(user['id'], user['username'], order['OrderNumber'], resp.status_code))
		except Exception as ex:
			return ExceptionUtils.error('''User: {}-{}, Get OrderItem: {} is error: {}'''.format(user['id'], user['username'], order['OrderNumber'], str(ex)))



	def getOrders(self, user):
		parameters = {
		'Action': 'GetOrders',
		'Format':'JSON',
		'Timestamp': LazadaApiHelper.getCurrentUTCTime(),
		'UserID': user['lazada_user_id'],
		'Version': '1.0',
		'CreatedBefore': LazadaApiHelper.getCurrentUTCTime()
		}

		parameters['Signature'] = LazadaApiHelper.generateSignature(parameters, user['lazada_api_key'])
		url = "{}?Action={}&CreatedBefore={}&Format={}&Timestamp={}&UserID={}&Version={}&Signature={}".format(
						LazadaAPI.ENDPOINT,
		 				parameters["Action"],
		 				LazadaApiHelper.formatTimestamp(parameters['CreatedBefore']),
		 				parameters["Format"],
		 				LazadaApiHelper.formatTimestamp(parameters["Timestamp"]),
		 				parameters["UserID"],
		 				parameters["Version"],
		 				parameters["Signature"])

		print (url)

		resp = requests.get(url)
		if resp.status_code == 200:
			response = json.loads(resp.text)
			if ('ErrorResponse' in response):
				return None

			data = response['SuccessResponse']['Body']
			if (data['Orders'] != None):
				return data['Orders']

		return None






