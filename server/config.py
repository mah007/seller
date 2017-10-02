
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
    LIMIT = 100          # limit 50 datas per request


class CronJob(object):
    AUTO_PRICE_TIME_INTEVAL = 25            # 25s
    GET_ORDER_TIME_INTEVAL = 2*60           # 5 minutes
    GET_PRODUCT_TIME_INTEVAL = 10*60        # 10 minutes
    PRICE_BY_TIME_INTERVAL = 5*60           # 5 minutes


class SkuConfig(object):
    DEFAULT_CERTAIN_SIZE = 5        # The limit of SKUs for adding of per user
    HISTORY_ENEMY_LIMIT_SIZE = 5    # The limit of size for tracking enemies of SKU's history


class OrderConfig(object):
    BARCODE_START_WITH_1 = "LMPDS"
    BARCODE_START_WITH_2 = "MPDS"


class ConstantConfig(object):
    PRODUCT_LAST_REQUEST = "product_last_request"   # Last request to get products from GetProductCronjob


class UserConfig(object):
    SUPER_ADMIN = "info@zakos.vn"


class AccountStatementConfig(object):
    ACCOUNT_STATEMENT = "1. Sao kê tài khoản"
    TRANSACTION_OVERVIEW = "2. Tổng quan giao dịch"
    MAX_RETRY_TIME = 3
    COLUMN_ORDER_NUMBER = 'A'
    COLUMN_SKU = 'C'
    COLUMN_ITEM_STATUS = 'E'
    COLUMN_TRACKING_NUMBER = 'G'
    COLUMN_SHIPMENT_TYPE = 'H'
    COLUMN_PAYMENT_METHOD = 'I'
    COLUMN_SALES_DELIVER = 'J'
    COLUMN_SALES_RETURN = 'K'
    COLUMN_WRONG_STATUS = 'L'
    COLUMN_WRONG_STATUS = 'L'
    COLUMN_SELLER_DELIVERY = 'M'
    COLUMN_PRODUCT_BUNDING = 'N'
    COLUMN_SUBSIDY = 'O'
    COLUMN_COMISSION = 'P'
    COLUMN_SUM_OF_FEE = 'AD'
    SCROLL_PAUSE_TIME = 1.0











