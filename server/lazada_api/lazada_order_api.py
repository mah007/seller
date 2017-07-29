import requests
import json
from lazada_api.lazada_api_helper import LazadaApiHelper
from config import LazadaAPI

class LazadaUserApi(object):

	def getOrder(self, order, user):
		parameters = {
		'Action': 'GetOrder',
		'Format':'JSON',
		'Timestamp': LazadaApiHelper.getCurrentUTCTime(),
		'UserID': user['lazada_user_id'],
		'Version': '1.0',
		'OrderId': '''["{}"]'''.format(order['id'])
		}

		parameters['Signature'] = LazadaApiHelper.generateSignature(parameters, user['lazada_api_key'])
		url = "{}/?Action={}&Format={}&Timestamp={}&UserID={}&Version={}&Signature={}&OrderId={}".format(
						LazadaAPI.ENDPOINT,
		 				parameters["Action"], 
		 				parameters["Format"], 
		 				LazadaApiHelper.formatTimestamp(parameters["Timestamp"]), 
		 				parameters["UserID"], 
		 				parameters["Version"],
		 				parameters["Signature"],
		 				parameters["OrderId"])

		resp = requests.get(url)
		if resp.status_code == 200:
			response = json.loads(resp.text)
			if ('ErrorResponse' in response):
				return None

			data = response['SuccessResponse']['Body']
			if (data['TotalProducts'] == 1):
				return data['Products'][0]
			
		return None










