
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


class RunnerConfig(object):
	TIME_INTEVAL = 25.0


class SkuConfig(object):
    DEFAULT_CERTAIN_SIZE = 5


class OrderConfig(object):
    BARCODE_START_WITH_1 = "LMPDS"
    BARCODE_START_WITH_2 = "MPDS"

class SkuHistoryConfig(object):
    HISTORY_SIZE = 5







