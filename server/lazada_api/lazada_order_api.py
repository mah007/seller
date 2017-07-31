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
			result = data['OrderItems']
			length = len(result)
			finalResult = []
			count = 1

			print (length)

			for o in range(length):
				print(o)

			if(result != None and length == 2):
				if (result[0]['TrackingCode'] == result[1]['TrackingCode']):
					count = count + 1
					result.remove(result[1])
				result[0]['Count'] = count
				finalResult.append(result[0])
				count = 1

			if (result != None and length > 2):										
				for i in range(0, length):
					for j in range(1, length):
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

			return finalResult

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









