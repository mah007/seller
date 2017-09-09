import datetime
import hmac, hashlib
from urllib.parse import urlencode, quote_plus


class LazadaApiHelper:

  # ----------------------------------------------------------------------------
  # Get Current UTC Time
  # Format: 2014-02-25T23:46:11+00:00
  # ----------------------------------------------------------------------------
  @classmethod
  def getCurrentUTCTime(self):
    utcnow = datetime.datetime.utcnow().isoformat()
    return utcnow[:-7] + "+00:00"

  # ----------------------------------------------------------------------------
  # Get Fixed Created After For Cron Job: This must be the minimun of time
  # which less then the first order of the seller
  # Format: 2014-02-25T23:46:11+00:00
  # ----------------------------------------------------------------------------
  @classmethod
  def getFixedCreatedAfterForCronJob():
    return "1990-02-25T23:46:11+00:00"

  # ----------------------------------------------------------------------------
  # Format Timestamp: format timestamp to using HTML character codes
  # ----------------------------------------------------------------------------
  @classmethod
  def formatTimestamp(self, timestamp):
    return timestamp.replace(":", "%3A").replace("+","%2B")

  # ----------------------------------------------------------------------------
  # Generate Signature: by lazada logic.
  # For more information visit lazada seller api document.
  # ----------------------------------------------------------------------------
  @classmethod
  def generateSignature(self, parameters, lazada_api_key):
    concatenated = urlencode(sorted(parameters.items()))
    key_bytes = bytes(lazada_api_key, 'utf-8')
    data_bytes = bytes(concatenated, 'utf-8')
    return hmac.new(key_bytes, data_bytes, hashlib.sha256).hexdigest()

  # ----------------------------------------------------------------------------
  # Generate Update Product XML:
  # Lazada XML format to update a product's special price
  # ----------------------------------------------------------------------------
  @classmethod
  def getUpdateProductSpecialPriceXML(self, sku, price):
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









