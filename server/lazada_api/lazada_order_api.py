import requests
import json
from lazada_api.lazada_api_helper import LazadaApiHelper
from config import LazadaAPI
from utils.exception_utils import ExceptionUtils



class LazadaOrderApi(object):

	#-----------------------------------------------------------------------------
	# Get order with limitation and offset
	#	Limit: 					limitation
	# Offset: 				offset
	# SortBy: 				created_at
	# SortDirection: 	Ascending (ASC)
	#-----------------------------------------------------------------------------
	def getOrders(self, user, offset):
		parameters = {
		'Action': 'GetOrders',
		'Format':'JSON',
		'Timestamp': LazadaApiHelper.getCurrentUTCTime(),
		'UserID': user['lazada_user_id'],
		'Version': LazadaAPI.VERSION,
		'Limit': LazadaAPI.LIMIT,
		'Offset': offset,
		'SortBy': 'updated_at',
		'SortDirection': 'ASC',
		'CreatedAfter': LazadaApiHelper.getFixedCreatedAfterForCronJob()
		}

		parameters['Signature'] = LazadaApiHelper.generateSignature(parameters, user['lazada_api_key'])
		url = "{}/?Action={}&Format={}&Timestamp={}&UserID={}&Version={}&Limit={}&Offset={}&SortBy={}&SortDirection={}&CreatedAfter={}&Signature={}".format(
						LazadaAPI.ENDPOINT,
		 				parameters["Action"],
		 				parameters["Format"],
		 				LazadaApiHelper.formatTimestamp(parameters["Timestamp"]),
		 				parameters["UserID"],
		 				parameters["Version"],
		 				parameters["Limit"],
		 				parameters["Offset"],
		 				parameters["SortBy"],
		 				parameters["SortDirection"],
		 				LazadaApiHelper.formatTimestamp(parameters["CreatedAfter"]),
		 				parameters["Signature"])

		try:
			resp = requests.get(url)
			if resp.status_code == 200:
				response = json.loads(resp.text)
				# Request API error
				if ('ErrorResponse' in response):
					errorMessage = ExceptionUtils.getBodyMessage(response)
					return None, '''User: {}-{}, Get-Orders: {}'''.format(user['username'], user['id'], errorMessage)

				# Request API Success
				return response['SuccessResponse']['Body']['Orders'], None

			# Request error
			return None, '''User: {}-{}, Get-Orders: {}'''.format(user['username'], user['id'], resp.status_code)
		except Exception as ex:
			return None, '''User: {}-{}, Get-Orders: {}'''.format(user['username'], user['id'], str(ex))

	#-----------------------------------------------------------------------------
	# Get order item by order id
	#-----------------------------------------------------------------------------
	def getOrderItems(self, user, orderId):
		parameters = {
		'Action': 'GetOrderItems',
		'Format':'json',
		'Timestamp': LazadaApiHelper.getCurrentUTCTime(),
		'UserID': user['lazada_user_id'],
		'Version': '1.0',
		'OrderId': str(orderId)
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
				if ('ErrorResponse' in response):
					errorMessage = ExceptionUtils.getBodyMessage(response)
					return None, '''User: {}-{}, Get-OrderItem: {}'''.format(user['username'], user['id'], errorMessage)

				# Request API Success
				return response['SuccessResponse']['Body']['OrderItems'], None

			# Request error
			return None, '''User: {}-{}, Get-OrderItems: {}'''.format(user['username'], user['id'], resp.status_code)
		except Exception as ex:
			return None, '''User: {}-{}, Get-OrderItems: {}'''.format(user['username'], user['id'], str(ex))

	#-----------------------------------------------------------------------------
	# Set Status: Ready to ship
	#-----------------------------------------------------------------------------
	def setStatusToPackedByMarketplace(self, user, orderItems):
		parameters = {
		'Action': 'SetStatusToPackedByMarketplace',
		'DeliveryType': 'dropship',
		'Format':'json',
		'OrderItemIds': '''[{}]'''.format(orderItems), # orderItems format should be string like this: 3,425,234
		'Timestamp': LazadaApiHelper.getCurrentUTCTime(),
		'UserID': user['lazada_user_id'],
		'Version': '1.0'
		}

		parameters['Signature'] = LazadaApiHelper.generateSignature(parameters, user['lazada_api_key'])
		url = "{}/?Action={}&DeliveryType={}&Format={}&OrderItemIds={}&&Timestamp={}&UserID={}&Version={}&Signature={}".format(
						LazadaAPI.ENDPOINT,
		 				parameters["Action"],
		 				parameters['DeliveryType'],
		 				parameters["Format"],
		 				parameters['OrderItemIds'],
		 				LazadaApiHelper.formatTimestamp(parameters["Timestamp"]),
		 				parameters["UserID"],
		 				parameters["Version"],
		 				parameters["Signature"])
		try:
			resp = requests.get(url)
			if resp.status_code == 200:
				response = json.loads(resp.text)
				if 'ErrorResponse' in response:
					return ExceptionUtils.error('''User: {}-{}, Set Status to Packed is error: {}'''.format(user['id'], user['username'], response['ErrorResponse']['Head']['ErrorMessage']))

				return ExceptionUtils.success("Set status to Parked is done") # Can't return None

			# Request except
			return ExceptionUtils.error('''User: {}-{}, Set Status to Packed is error: {}'''.format(user['id'], user['username'], resp.status_code))
		except Exception as ex:
			return ExceptionUtils.error('''User: {}-{}, Set Status to Packed is error: {}'''.format(user['id'], user['username'], str(ex)))


	#-----------------------------------------------------------------------------
	# Set Status To Packed By Market place
	#-----------------------------------------------------------------------------
	def setStatusToReadyToShip(self, user, orderItems):
		parameters = {
		'Action': 'SetStatusToReadyToShip',
		'Format':'json',
		'Timestamp': LazadaApiHelper.getCurrentUTCTime(),
		'UserID': user['lazada_user_id'],
		'Version': '1.0',
		'DeliveryType': 'dropship',
		'OrderItemIds': '''[{}]'''.format(orderItems) # orderItems format should be string like this: 3,425,234
		}

		parameters['Signature'] = LazadaApiHelper.generateSignature(parameters, user['lazada_api_key'])
		url = "{}/?Action={}&Format={}&DeliveryType={}&OrderItemIds={}&&Timestamp={}&UserID={}&Version={}&Signature={}".format(
						LazadaAPI.ENDPOINT,
		 				parameters["Action"],
		 				parameters["Format"],
		 				parameters['DeliveryType'],
		 				parameters['OrderItemIds'],
		 				LazadaApiHelper.formatTimestamp(parameters["Timestamp"]),
		 				parameters["UserID"],
		 				parameters["Version"],
		 				parameters["Signature"])
		try:
			resp = requests.get(url)
			if resp.status_code == 200:
				response = json.loads(resp.text)
				if 'ErrorResponse' in response:
					return ExceptionUtils.error('''User: {}-{}, Set Status to Ready-To-Ship is error: {}'''.format(user['id'], user['username'], response['ErrorResponse']['Head']['ErrorMessage']))

				return ExceptionUtils.success("Set status to Ready-to-ship is done") # Can't return None

			# Request except
			return ExceptionUtils.error('''User: {}-{}, Set Status to Ready-To-Ship is error: {}'''.format(user['id'], user['username'], resp.status_code))
		except Exception as ex:
			return ExceptionUtils.error('''User: {}-{}, Set Status to Ready-To-Ship is error: {}'''.format(user['id'], user['username'], str(ex)))















