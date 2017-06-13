from database.sku_dao import SkuDao
from eve import Eve


if __name__ == "__main__":
	skudao = SkuDao()
	skudao.createTable()

	app = Eve()
	app.run()