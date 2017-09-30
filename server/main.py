from managers.sku_manager import SkuManager
from managers.user_manager import UserManager
from managers.order_manager import OrderManager
from managers.constant_manager import ConstantManager
from managers.price_by_time_manager import PriceByTimeManager
from managers.product_manager import ProductManager
from managers.account_statement_manager import AccountStatementManager
from apis.sku_api import SkuAPI
from apis.user_api import UserAPI
from apis.order_api import OrderAPI
from apis.price_by_time_api import PriceByTimeAPI
from apis.product_api import ProductAPI
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin

from utils.timestamp_utils import TimestampUtils
from database.user_dao import UserDao
from database.account_statement_dao import AccountStatementDao
from cronjob.process_account_statement import ProcessAccountStatement

app = Flask(__name__)
CORS(app) # Should allow CORS only for our domain.
app.register_blueprint(SkuAPI)
app.register_blueprint(UserAPI)
app.register_blueprint(OrderAPI)
app.register_blueprint(PriceByTimeAPI)
app.register_blueprint(ProductAPI)

if __name__ == "__main__":
  skuManager = SkuManager()
  userManager = UserManager()
  orderManager = OrderManager()
  constantManager = ConstantManager()
  priceByTimeManager = PriceByTimeManager()
  productManager = ProductManager()
  accountStatementManager = AccountStatementManager()
  skuManager.initialize()
  userManager.initialize()
  orderManager.initialize()
  constantManager.initialize()
  priceByTimeManager.initialize()
  productManager.initialize()
  accountStatementManager.initialize()

  # Process Account Statement for test
  userDao = UserDao()
  superAdmin = userDao.getSuperAdmin()

  # Insert Account Statement
  accountStatement = {
    "excel_url": "./resources/VN10VI4 2017-08-01-14.xlsx",
    "start_date": "2017-08-01 00:00:00",
    "end_date": "2017-08-014 00:00:00",
    "sales_revenue": 13780000,
    "income": 0,
    "created_at": TimestampUtils.getCurrentDatatime(),
  }
  userDao = UserDao()
  superAdmin = userDao.getSuperAdmin()
  if 'error' in superAdmin:
    print(superAdmin)
  else:
    accountStatementDao = AccountStatementDao()
    accountStatementDao.insert(superAdmin, accountStatement)

  # Run account statement process
  accountStatementDao = AccountStatementDao()
  accountStatement = accountStatementDao.getFirstAccountStatementForTest(superAdmin)
  if (superAdmin != None and accountStatement != None):
    clone = ProcessAccountStatement({"user": superAdmin, "account_statement": accountStatement})
    try:
      clone.start()
    except Exception as ex:
      clone.join(0)
      print ("Error: unable to start thread: ", ex)
  else:
    print(superAdmin, accountStatement)

  # app.run(debug=True, threaded=True)
  # app.run(host='0.0.0.0', debug=True, port=5000, threaded=True)







