from database.sku_dao import SkuDao


class SkuManager(object):

	def initialize(self):
		skudao = SkuDao()
		skudao.createTable()


	def insertSku(self, sku):
		skudao = SkuDao()
		skudao.insert(sku)

