import time
from managers.sku_manager import SkuManager
from managers.user_manager import UserManager
from managers.order_manager import OrderManager
from managers.constant_manager import ConstantManager
from managers.price_balancer_manager import PriceBalancerManager
from apis.sku_api import SkuAPI
from apis.user_api import UserAPI
from apis.order_api import OrderAPI
from apis.price_balancer_api import PriceBalancerAPI
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from time import sleep
from lazada_api.lazada_order_api import LazadaOrderApi

app = Flask(__name__)
CORS(app) # Should allow CORS only for our domain.
app.register_blueprint(SkuAPI)
app.register_blueprint(UserAPI)
app.register_blueprint(OrderAPI)
app.register_blueprint(PriceBalancerAPI)

if __name__ == "__main__":
  skuManager = SkuManager()
  userManager = UserManager()
  orderManager = OrderManager()
  constantManager = ConstantManager()
  priceBalancerManager = PriceBalancerManager()
  skuManager.initialize()
  userManager.initialize()
  orderManager.initialize()
  constantManager.initialize()
  priceBalancerManager.initialize()

  # app.run(debug=True, threaded=True)
  app.run(host='0.0.0.0', debug=True, port=5000, threaded=True)







