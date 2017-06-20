from managers.sku_manager import SkuManager
from managers.user_manager import UserManager
from apis.sku_api import SkuAPI
from flask import Flask
from flask_cors import CORS, cross_origin
from runners.price_automatically_runner import PriceAutomaticallyRunner

app = Flask(__name__)
CORS(app)	# Should allow CORS only for our domain.
app.register_blueprint(SkuAPI)

if __name__ == "__main__":
	skuManager = SkuManager()
	userManager = UserManager()
	skuManager.initialize()
	userManager.initialize()

	# priceAutomatically = PriceAutomaticallyRunner()
	# priceAutomatically.run()
	
	app.run(debug=True)


	