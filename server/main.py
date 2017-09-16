import time
from managers.sku_manager import SkuManager
from managers.user_manager import UserManager
from managers.order_manager import OrderManager
from managers.constant_manager import ConstantManager
from managers.price_by_time_manager import PriceByTimeManager
from managers.product_manager import ProductManager
from apis.sku_api import SkuAPI
from apis.user_api import UserAPI
from apis.order_api import OrderAPI
from apis.price_by_time_api import PriceByTimeAPI
from apis.price_by_time_api import ProductAPI
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin

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
  skuManager.initialize()
  userManager.initialize()
  orderManager.initialize()
  constantManager.initialize()
  priceByTimeManager.initialize()
  productManager.initialize()

  app.run(debug=True, threaded=True)
  # app.run(host='0.0.0.0', debug=True, port=5000, threaded=True)







