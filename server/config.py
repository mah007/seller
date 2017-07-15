
class Database(object):
	mysql = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'lazada',
    'use_unicode':True,
    'charset': 'utf8'
  }

class LazadaAPI(object):
	ENDPOINT = "https://api.sellercenter.lazada.vn"


class RunnerConfig(object):
	TIME_INTEVAL = 25.0