import time
import json
import threading
from lazada_api.lazada_sku_api import LazadaSkuApi
from database.price_by_time_dao import PriceByTimeDao
from utils.timestamp_utils import TimestampUtils

# For caching memory
lazadaSkuApi = LazadaSkuApi()
priceByTimeDao = PriceByTimeDao()

class PriceByTimeWorker(threading.Thread):

  def __init__(self, kwargs):
    threading.Thread.__init__(self)
    self.kwargs = kwargs

  def run(self):
    user = self.kwargs['user']
    print('''*********** {} is running ***********'''.format(user['lazada_user_name']))

    # Get all skus of price by time
    priceByTimeSkus = priceByTimeDao.getAll(user);
    if 'error' in priceByTimeSkus:
      print(priceByTimeSkus)
      return

    for priceByTimeSku in enumerate(priceByTimeSkus):
      if not priceByTimeSku['price_by_time']:
        continue

      priceByTimes = json.loads(priceByTimeSku['price_by_time'])
      self.updateSpcialPriceByPriceByTimes(user, priceByTimeSku, priceByTimes)

  #-----------------------------------------------------------------------------
  # The algorithm
  #-----------------------------------------------------------------------------
  def updateSpcialPriceByPriceByTimes(self, user, priceByTimeSku, priceByTimes):
    if not priceByTimes or len(priceByTimes) <= 0:
      return

    newSpecialPrice = priceByTimeSku['special_price']
    for index, priceByTime in priceByTimes:
      isOnTime = False
      if len(priceByTimeSkus) < index + 1:
        isOnTime = self.isOnTime(priceByTime, priceByTimes[index + 1], False)
      else:
        isOnTime = self.isOnTime(priceByTime, priceByTimes[0], True)

      if isOnTime == True:
        newSpecialPrice = priceByTime['price']

    print('''newSpecialPrice: {} currentSpecialPrice: {} '''.format(newSpecialPrice, priceByTimeSku['special_price']))
    if newSpecialPrice != priceByTimeSku['special_price']:
      self.updateSpecialPrice(user, priceByTimeSku, newSpecialPrice)

  #-----------------------------------------------------------------------------
  # Only call this function when the current time is on time of PriceBytime
  # Todo list:
  # 1. Update product special price on Lazada.
  # 2. Update prciceByTime special on local.
  # Return Void
  #-----------------------------------------------------------------------------
  def updateSpecialPrice(self, user, priceByTimeSku, newSpecialPrice):
    print('''Update sku: {} with special price: {} '''.format(priceByTimeSku['sku'], newSpecialPrice))

    # Update lazada special price
    result = lazadaSkuApi.updateProductSpecialPrice(priceByTimeSku, user, newSpecialPrice)
    if 'error' in result:
      print(result)
      return

    # Update PriceByTime special
    result = priceByTimeDao.updateSpecialPrice(priceByTimeSku, user, newSpecialPrice)
    if 'error' in result:
      print(result)

  #-----------------------------------------------------------------------------
  # Detemine whether current time is on PriceByTime's period.
  # PriceByTime format: hour:minute ==> 10:45
  # Return Boolean
  #-----------------------------------------------------------------------------
  def isOnTime(self, priceByTime, nextPriceByTime, isNextDay):
    if not priceByTime or not nextPriceByTime:
      return False
    if not 'from' in priceByTime or not 'from' in nextPriceByTime:
      return False

    timeArray = priceByTime['from'].split(':')
    nextTimeArray = nextPriceByTime['from'].split(':')
    if len(timeArray) != 2 or len(nextPriceByTime) != 2:
      return False

    hour = int(timeArray[0])
    minute = int(timeArray[1])
    currentHour = TimestampUtils.getVietNamCurrentHour()
    currentMinute = TimestampUtils.getVietnamCurrentMinute()
    nextPriceByTimeHour = int(nextTimeArray[0])
    print(hour, minute, currentHour, currentMinute, nextPriceByTimeHour)

    if currentHour - hour > 0:
      return True     # Set 3:30 and current time is 4:0
    if currentHour - hour == 0 and currentMinute - minute >= 0:
      return True     # Set 3:30 and current time is 3:40
    if currentHour < nextPriceByTimeHour and isNextDay == True:
      return True     # Set 21:30 and current time is 1:0 of next day.

    return False













