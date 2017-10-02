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
  def getFixedCreatedAfterForCronJob(self):
    return "1990-02-25T23:46:11+00:00"

  # ----------------------------------------------------------------------------
  # Format to lazada timestamp: example: 2017-09-25T23:17:10+00:00
  #
  # Before Timestamp: 2017-09-25 23:17:10
  # After Timestamp: 2017-09-25T23:17:10+00:00
  # ----------------------------------------------------------------------------
  @classmethod
  def formatToLazadaTimestamp(self, timestamp):
    myDatatime = datetime.datetime.strptime(str(timestamp), "%Y-%m-%d %H:%M:%S")
    timestamp = myDatatime - datetime.timedelta(hours=7)
    return "{}+00:00".format(str(timestamp).replace(" ", "T"))

  # ----------------------------------------------------------------------------
  # Fixed updated after using for cronjob only
  #
  # This time is using for get all products and orders before this one.
  # Format: 2016-01-01 00:00:00
  #
  # NOTE: we dont using format "1990-02-25T23:46:11+00:00" for this because
  # Order updated_at is different format, check getOrderWorker for more detail
  # ----------------------------------------------------------------------------
  @classmethod
  def getFixedUpdatedAfterForCronJob(self):
    return "2016-01-01 00:00:00"

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









