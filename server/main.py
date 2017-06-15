from managers.sku_manager import SkuManager
from managers.user_manager import UserManager
from apis.sku_api import SkuAPI
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.register_blueprint(SkuAPI)

if __name__ == "__main__":
	skuManager = SkuManager()
	skuManager.initialize()
	userManager = UserManager()
	userManager.initialize()

	app.run(debug=True)
	