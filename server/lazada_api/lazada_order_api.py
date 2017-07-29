import requests
import json
from lazada_api.lazada_api_helper import LazadaApiHelper
from config import LazadaAPI

class LazadaOrderApi(object):

	def getOrder(self, order, user):
		parameters = {
		'Action': 'GetOrder',
		'Format':'JSON',
		'Timestamp': LazadaApiHelper.getCurrentUTCTime(),
		'UserID': user['lazada_user_id'],
		'Version': '1.0',
		'OrderId': (order['id'])
		}

		parameters['Signature'] = LazadaApiHelper.generateSignature(parameters, user['lazada_api_key'])
		url = "{}?Action={}&Format={}&OrderId={}&Timestamp={}&UserID={}&Version={}&Signature={}".format(
						LazadaAPI.ENDPOINT,
		 				parameters["Action"], 
		 				parameters["Format"], 
		 				parameters["OrderId"],
		 				LazadaApiHelper.formatTimestamp(parameters["Timestamp"]), 
		 				parameters["UserID"], 
		 				parameters["Version"],
		 				parameters["Signature"],)

		resp = requests.get(url)
		if resp.status_code == 200:
			response = json.loads(resp.text)
			if ('ErrorResponse' in response):
				return None

			data = response['SuccessResponse']['Body']
			if (data['Orders'] != None):
				return data['Orders']

		print(url)
				
			
		return None

	def getOrderItems(self, order, user):
		parameters = {
		'Action': 'GetOrderItems',
		'Format':'JSON',
		'Timestamp': LazadaApiHelper.getCurrentUTCTime(),
		'UserID': user['lazada_user_id'],
		'Version': '1.0',
		'OrderId': (order['id'])
		}

		parameters['Signature'] = LazadaApiHelper.generateSignature(parameters, user['lazada_api_key'])
		url = "{}?Action={}&Format={}&Timestamp={}&UserID={}&Version={}&Signature={}&OrderId={}".format(
						LazadaAPI.ENDPOINT,
		 				parameters["Action"], 
		 				parameters["Format"], 
		 				LazadaApiHelper.formatTimestamp(parameters["Timestamp"]), 
		 				parameters["UserID"], 
		 				parameters["Version"],
		 				parameters["Signature"],
		 				parameters['OrderId'])

		resp = requests.get(url)
		if resp.status_code == 200:
			response = json.loads(resp.text)
			if ('ErrorResponse' in response):
				return None

			data = response['SuccessResponse']['Body']
			if (data['OrderItems'] != None):
				return data['OrderItems']
				
			
		return None


	# def initialize(self):
	# 	 user = {
	# 	  'lazada_api_key': 'jusjWjdv13rre3RxH9b-cXmmA7B9cQQh4jtiLcDyAqX-8PMkhutFeRsv',
	# 	  'lazada_user_id': 'info@zakos.vn'
	# 	 }
	# 	 order = {
	# 	 	'id': '111682924'
	# 	 }
	# 	 result = self.getOrderItems(order, user)
	# 	 print(result)









