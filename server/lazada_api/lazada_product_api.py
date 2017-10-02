import requests
import json
from config import LazadaAPI
from utils.lazada_api_helper import LazadaApiHelper
from utils.exception_utils import ExceptionUtils



class LazadaProductApi(object):

	#-----------------------------------------------------------------------------
	# Get Produts by UpdatedAfter
	#-----------------------------------------------------------------------------
	def getProductByUpdatedAfter(self, user, offset, updatedAfter):
		parameters = {
		'Action': 'GetProducts',
		'Format':'JSON',
		'Timestamp': LazadaApiHelper.getCurrentUTCTime(),
		'UserID': user['lazada_user_id'],
		'Version': '1.0',
		'UpdatedAfter': LazadaApiHelper.formatToLazadaTimestamp(updatedAfter),
		'Filter': 'all',
		'Limit': LazadaAPI.LIMIT,
		'Offset': offset
		}

		parameters['Signature'] = LazadaApiHelper.generateSignature(parameters, user['lazada_api_key'])
		url = "{}/?Action={}&Format={}&Timestamp={}&UserID={}&Version={}&Signature={}&UpdatedAfter={}&Filter={}&Offset={}&Limit={}".format(
						LazadaAPI.ENDPOINT,
		 				parameters["Action"],
		 				parameters["Format"],
		 				LazadaApiHelper.formatTimestamp(parameters["Timestamp"]),
		 				parameters["UserID"],
		 				parameters["Version"],
		 				parameters["Signature"],
		 				LazadaApiHelper.formatTimestamp(parameters["UpdatedAfter"]),
		 				parameters["Filter"],
		 				parameters["Offset"],
		 				parameters["Limit"])
		try:
			resp = requests.get(url)
			if resp.status_code == 200:
				response = json.loads(resp.text)
				if ('ErrorResponse' in response):
					return None, ExceptionUtils.returnError('''Get Products is error: ''', response)

				data = response['SuccessResponse']['Body']
				return data['Products'], None

			return None, '''Get Products is error: {}'''.format(resp.status_code)
		except Exception as ex:
			return None, '''Get Products is error: {}'''.format(str(ex))



