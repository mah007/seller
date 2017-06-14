from database.sku_dao import SkuDao
from apis.sku_api import SkuAPI
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.register_blueprint(SkuAPI)

if __name__ == "__main__":
	skudao = SkuDao()
	skudao.createTable()

	app.run(debug=True)