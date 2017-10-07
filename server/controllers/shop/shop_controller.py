from functions.validation import Validation
from utils.response_utils import ResponseUtils
from database.shop_dao import ShopDao
from lazada_api.lazada_statistic_api import LazadaStatisticApi


class ShopController(object):

    #---------------------------------------------------------------------------
    # Create shop
    #---------------------------------------------------------------------------
    def createShop(self, token, shop):
        user, exception = Validation.validateToken(token)
        if (exception != None):
            return ResponseUtils.returnError(exception)

        # Test api key
        lazadaStatisticApi = LazadaStatisticApi()
        result, exception = lazadaStatisticApi.getStatistic(user, shop)
        if (exception != None):
            return ResponseUtils.returnError("Lazada email or api-key is incorrect")

        # create shop
        shopDao = ShopDao()
        result, exception = shopDao.insert(user, shop)
        if (exception != None):
            return ResponseUtils.returnError(exception)

        # Start cronjob

        # Done
        return ResponseUtils.returnSuccess(result)