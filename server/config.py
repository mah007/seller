
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
    LIMIT = 30          # limit 50 datas per request


class CronJob(object):
    AUTO_PRICE_TIME_INTEVAL = 25            # 25s
    GET_ORDER_TIME_INTEVAL = 100*60           # 10 minutes
    GET_PRODUCT_TIME_INTEVAL = 10*60        # 10 minutes
    PRICE_BY_TIME_INTERVAL = 5*60           # 5 minutes


class SkuConfig(object):
    DEFAULT_CERTAIN_SIZE = 5        # The limit of SKUs for adding of per user
    HISTORY_ENEMY_LIMIT_SIZE = 5    # The limit of size for tracking enemies of SKU's history


class OrderConfig(object):
    BARCODE_START_WITH_1 = "LMPDS"
    BARCODE_START_WITH_2 = "MPDS"


class ConstantConfig(object):
    ORDER_OFFSET = "order_offset"
    PRODUCT_OFFSET = "product_offset"


class UserConfig(object):
    SUPER_ADMIN = "info@zakos.vn"










