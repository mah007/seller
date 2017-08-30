import requests
import json
from config import LazadaAPI
from lazada_api.lazada_api_helper import LazadaApiHelper
from utils.exception_utils import ExceptionUtils

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
		url = "{}/?Action={}&Format={}&Timestamp={}&UserID={}&Version={}&SkuSellerList={}&Signature={}".format(
						LazadaAPI.ENDPOINT,
		 				parameters["Action"],
		 				parameters["Format"],
		 				LazadaApiHelper.formatTimestamp(parameters["Timestamp"]),
		 				parameters["UserID"],
		 				parameters["Version"],
		 				parameters["SkuSellerList"],
		 				parameters["Signature"])

		try:
			resp = requests.get(url)
			if resp.status_code == 200:
				response = json.loads(resp.text)
				if 'SuccessResponse' in response:
					data = response['SuccessResponse']['Body']
					if data['TotalProducts'] == 1:
						return data['Products'][0]
					else:
						return ExceptionUtils.error('''Invalide Seller SKU !''')
				else:
					return ExceptionUtils.returnError('''Can't get this product with error: ''', response)
			else:
				return ExceptionUtils.error('''Get product got error's response-code: {}'''.format(resp.status_code))
		except Exception as ex:
			return ExceptionUtils.error('''Get product got exception: {}'''.format(str(ex)))


	def updateProductSpecialPrice(self, sku, user, newSpecialPrice):
		parameters = {
		'Action': 'UpdateProduct',
		'Format':'JSON',
		'Timestamp': LazadaApiHelper.getCurrentUTCTime(),
		'UserID': user['lazada_user_id'],
		'Version': '1.0'
		}

		parameters['Signature'] = LazadaApiHelper.generateSignature(parameters, user['lazada_api_key'])
		url = "{}/?Action={}&Format={}&Timestamp={}&UserID={}&Version={}&Signature={}".format(
						LazadaAPI.ENDPOINT,
		 				parameters["Action"],
		 				parameters["Format"],
		 				LazadaApiHelper.formatTimestamp(parameters["Timestamp"]),
		 				parameters["UserID"],
		 				parameters["Version"],
		 				parameters["Signature"])

		# Must use xmlBody to update
		xmlBody = LazadaApiHelper.generateUpdateProductXML(sku, newSpecialPrice)

		try:
			resp = requests.post(url, data=xmlBody)
			if resp.status_code != 200:
				return ExceptionUtils.error('''Request error with response-code: {}'''.format(resp.status_code))

			response = resp.json()
			if ('SuccessResponse' in response):
				return ExceptionUtils.success("Update procduct special price success")
			else:
				return ExceptionUtils.returnError("Update product special price error: ", response)
		except Exception as ex:
			return ExceptionUtils.error('''Update product special price got exception: {}'''.format(str(ex)))








