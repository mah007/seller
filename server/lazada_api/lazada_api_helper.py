import datetime
import urllib
from hashlib import sha256
from hmac import HMAC


class LazadaApiHelper:

	@classmethod
	def getCurrentUTCTime(self):
		utcnow = datetime.datetime.utcnow().isoformat()
		return utcnow[:-7] + "+00:00"

	@classmethod
	def formatTimestamp(self, timestamp):
		return timestamp.replace(":", "%3A").replace("+","%2B")

	@classmethod
	def generateSignature(self, parameters, lazada_api_key):
		concatenated = urllib.urlencode(sorted(parameters.items()))
		return HMAC(lazada_api_key, concatenated, sha256).hexdigest()

	@classmethod
	def generateUpdateProductXML(self, sku, price):
		return '''<?xml version="1.0" encoding="UTF-8" ?>
			<Request>
			    <Product>
			        <Skus>
			            <Sku>
			                <SellerSku>{}</SellerSku>
			                <special_price>{}</special_price>
			            </Sku>
			        </Skus>
			    </Product>
			</Request>'''.format(sku['sku'], price)









