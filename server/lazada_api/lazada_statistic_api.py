import json
import requests
from config import LazadaAPI
from utils.exception_utils import ExceptionUtils
from utils.lazada_api_helper import LazadaApiHelper

class LazadaStatisticApi(object):

  def getStatistic(self, user, shop):
    parameters = {
      'Action': 'GetStatistics',
      'Format':'JSON',
      'Timestamp': LazadaApiHelper.getCurrentUTCTime(),
      'UserID': shop['email'],
      'Version': '1.0'
    }

    parameters['Signature'] = LazadaApiHelper.generateSignature(parameters, shop['api_key'])
    url = "{}/?Action={}&Format={}&Timestamp={}&UserID={}&Version={}&Signature={}".format(
            LazadaAPI.ENDPOINT,
            parameters["Action"],
            parameters["Format"],
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
          return None, '''User: {}-{}, Get-Statistic: {}'''.format(user['username'], user['id'], errorMessage)

        # Request API Success
        return response['SuccessResponse']['Body'], None

      # Request error
      return None, '''User: {}-{}, Get-Statistic: {}'''.format(user['username'], user['id'], resp.status_code)
    except Exception as ex:
      return None, '''User: {}-{}, Get-Statistic: {}'''.format(user['username'], user['id'], str(ex))

















