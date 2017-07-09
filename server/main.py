import time
from managers.sku_manager import SkuManager
from managers.user_manager import UserManager
from apis.sku_api import SkuAPI
from apis.user_api import UserAPI
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
from time import sleep


app = Flask(__name__)
CORS(app)	# Should allow CORS only for our domain.
app.register_blueprint(SkuAPI)
app.register_blueprint(UserAPI)

if __name__ == "__main__":
  skuManager = SkuManager()
  userManager = UserManager()
  skuManager.initialize()
  userManager.initialize()

  app.run(debug=True)







