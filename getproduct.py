import urllib
import requests
import json

import time
import arrow
import pytz
import datetime

from hashlib import sha256
from hmac import HMAC
from pytz.reference import UTC

def getCurrentUTCTime():
	utcnow = datetime.datetime.utcnow().isoformat()
	return utcnow[:-7] + "+00:00"

def formatTimestamp(timestamp):
	return timestamp.replace(":", "%3A").replace("+","%2B")

def formatUrl(parameters):
	return "https://api.sellercenter.lazada.vn/?Action={}&Filter={}&Format={}&Timestamp={}&UserID={}&Version={}&Signature={}".format(
	 				parameters["Action"], 
	 				parameters["Filter"], 
	 				parameters["Format"], 
	 				formatTimestamp(parameters["Timestamp"]), 
	 				parameters["UserID"], 
	 				parameters["Version"], 
	 				parameters["Signature"])


if __name__ == "__main__":
	api_key = 'your-api-key'
	parameters = {
	'Action': 'GetProducts',
	'Filter': 'all',
	'Format':'JSON',
	'Timestamp': getCurrentUTCTime(),
	'UserID': 'info@lakami.vn',
	'Version': '1.0',
	}

	concatenated = urllib.urlencode(sorted(parameters.items()))
	parameters['Signature'] = HMAC(api_key, concatenated, sha256).hexdigest()
	print(parameters)

	resp = requests.get(formatUrl(parameters))
	if resp.status_code == 200:
		print(resp.text)
		# jsonData = json.loads(resp.text)
		# print jsonData
	else:
		print ("RESPONSE CODE %d" % resp.status_code)
		print ("RESPONSE CODE %s" % dataBody)
		print ("RESPONSE CODE %s" % self.headers)
		print ("------------------------------------")







