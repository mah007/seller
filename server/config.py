
class Database(object):
    mysql = {
    'user': 'root',
    'password': '1234',
    'host': '',
    'database': 'lazada',
    'use_unicode':True,
    'charset': 'utf8'
  }


class LazadaAPI(object):
    ENDPOINT = "https://api.sellercenter.lazada.vn"
    VERSION = '1.0'
    LIMIT = 50          # limit 50 datas per request


class CronJob(object):
    AUTO_PRICE_TIME_INTEVAL = 25            # 25s
    GET_ORDER_TIME_INTEVAL = 5*60           # 5 minutes
    GET_PRODUCT_TIME_INTEVAL = 24*60*60     # 24 hours


class SkuConfig(object):
    DEFAULT_CERTAIN_SIZE = 5        # The limit of SKUs for adding of per user
    HISTORY_ENEMY_LIMIT_SIZE = 5    # The limit of size for tracking enemies of SKU's history


class OrderConfig(object):
    BARCODE_START_WITH_1 = "LMPDS"
    BARCODE_START_WITH_2 = "MPDS"


class ConstantConfig(object):
    ORDER_OFFSET = "order_offset"
    PRODUCT_OFFSET = "order_offset"










