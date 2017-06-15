import requests
import json
from lazada_api.lazada_api_helper import LazadaApiHelper

class LazadaSkuApi(object):

	def getSku(self, sku, user):
		parameters = {
		'Action': 'GetProducts',
		'Format':'JSON',
		'Timestamp': LazadaApiHelper.getCurrentUTCTime(),
		'UserID': user['lazada_user_id'],
		'Version': '1.0',
		'SkuSellerList': '''["{}"]'''.format(sku['sku'])
		}

		parameters['Signature'] = LazadaApiHelper.generateSignature(parameters, user['lazada_api_key'])
		url = "https://api.sellercenter.lazada.vn/?Action={}&Format={}&Timestamp={}&UserID={}&Version={}&SkuSellerList={}&Signature={}".format(
		 				parameters["Action"], 
		 				parameters["Format"], 
		 				LazadaApiHelper.formatTimestamp(parameters["Timestamp"]), 
		 				parameters["UserID"], 
		 				parameters["Version"],
		 				parameters["SkuSellerList"],
		 				parameters["Signature"])

		resp = requests.get(url)
		if resp.status_code == 200:
			response = json.loads(resp.text)
			if ('ErrorResponse' in response):
				return None

			date = response['SuccessResponse']['Body']
			if (data['TotalProducts'] == 1):
				return data['Products'][0]
			
		return None







