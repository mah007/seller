import requests
import json
from lazada_api.lazada_api_helper import LazadaApiHelper
from config import LazadaAPI
from utils.exception_utils import ExceptionUtils



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
		url = "{}/?Action={}&CreatedBefore={}&Format={}&Status={}&Timestamp={}&UserID={}&Version={}&Signature={}".format(
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
		url = "{}/?Action={}&Format={}&OrderId={}&Timestamp={}&UserID={}&Version={}&Signature={}".format(
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

				return response['SuccessResponse']['Body']['OrderItems']

			# Request except
			return ExceptionUtils.error('''User: {}-{}, Get OrderItem: {} is error: {}'''.format(user['id'], user['username'], order['OrderNumber'], resp.status_code))
		except Exception as ex:
			return ExceptionUtils.error('''User: {}-{}, Get OrderItem: {} is error: {}'''.format(user['id'], user['username'], order['OrderNumber'], str(ex)))


	#-----------------------------------------------------------------------------
	# Set Status: Ready to ship
	#-----------------------------------------------------------------------------
	def setStatusToPackedByMarketplace(self, user, orderItems, shippingProvider):
		parameters = {
		'Action': 'SetStatusToPackedByMarketplace',
		'Format':'JSON',
		'Timestamp': LazadaApiHelper.getCurrentUTCTime(),
		'UserID': user['lazada_user_id'],
		'Version': '1.0',
		'DeliveryType': 'dropship',
		'OrderItemIds': '''[{}]'''.format(orderItems),
		'ShippingProvider': shippingProvider.replace(" ","%20")
		}

		parameters['Signature'] = LazadaApiHelper.generateSignature(parameters, user['lazada_api_key'])
		url = "{}/?Action={}&Format={}&DeliveryType={}&OrderItemIds={}&ShippingProvider={}&Timestamp={}&UserID={}&Version={}&Signature={}".format(
						LazadaAPI.ENDPOINT,
		 				parameters["Action"],
		 				parameters["Format"],
		 				parameters['DeliveryType'],
		 				parameters['OrderItemIds'],
		 				parameters['ShippingProvider'],
		 				LazadaApiHelper.formatTimestamp(parameters["Timestamp"]),
		 				parameters["UserID"],
		 				parameters["Version"],
		 				parameters["Signature"])

		print(url)
		try:
			resp = requests.get(url)
			if resp.status_code == 200:
				response = json.loads(resp.text)
				# Lazada return exception
				if 'ErrorResponse' in response:
					return ExceptionUtils.error('''User: {}-{}, Set Status to Packed is error: {}'''.format(user['id'], user['username'], response['ErrorResponse']['Head']['ErrorMessage']))

				return None # None likely is done

			# Request except
			return ExceptionUtils.error('''User: {}-{}, Set Status to Packed is error: {}'''.format(user['id'], user['username'], resp.status_code))
		except Exception as ex:
			return ExceptionUtils.error('''User: {}-{}, Set Status to Packed is error: {}'''.format(user['id'], user['username'], str(ex)))


	#-----------------------------------------------------------------------------
	# Set Status To Packed By Market place
	#-----------------------------------------------------------------------------
	def setStatusToReadyToShip(self, user, orderItems, shippingProvider):
		parameters = {
		'Action': 'SetStatusToReadyToShip',
		'Format':'json',
		'Timestamp': LazadaApiHelper.getCurrentUTCTime(),
		'UserID': user['lazada_user_id'],
		'Version': '1.0',
		'DeliveryType': 'dropship',
		'OrderItemIds': '''[{}]'''.format(orderItems), # orderItems format should be string like this: 3,425,234
		'ShippingProvider': shippingProvider
		}

		parameters['Signature'] = LazadaApiHelper.generateSignature(parameters, user['lazada_api_key'])
		url = "{}/?Action={}&Format={}&DeliveryType={}&OrderItemIds={}&ShippingProvider={}&Timestamp={}&UserID={}&Version={}&Signature={}".format(
						LazadaAPI.ENDPOINT,
		 				parameters["Action"],
		 				parameters["Format"],
		 				parameters['DeliveryType'],
		 				parameters['OrderItemIds'],
		 				parameters['ShippingProvider'],
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
					return ExceptionUtils.error('''User: {}-{}, Set Status to Ready-To-Ship is error: {}'''.format(user['id'], user['username'], response['ErrorResponse']['Head']['ErrorMessage']))

				return None # None likely is done

			# Request except
			return ExceptionUtils.error('''User: {}-{}, Set Status to Ready-To-Ship is error: {}'''.format(user['id'], user['username'], resp.status_code))
		except Exception as ex:
			return ExceptionUtils.error('''User: {}-{}, Set Status to Ready-To-Ship is error: {}'''.format(user['id'], user['username'], str(ex)))







