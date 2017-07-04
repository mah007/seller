from database.sku_dao import SkuDao


class SkuManager(object):

	def initialize(self):
		skudao = SkuDao()
		skudao.createTable()


	def insertSku(self, sku, user):
		skudao = SkuDao()
		skudao.insert(sku, user)


	def deleteSku(self, sku):
		skudao = SkuDao()
		skudao.delete(sku)


	def getAll(self, token):
		skudao = SkuDao()
		return skudao.getAll()


	def updateSkuState(self, sku):
		skudao = SkuDao()
		skudao.updateState(sku)

	def getById(self, id):
		skudao = SkuDao()
		return skudao.getById(id)

	def updateSku(self, sku):
		skudao = SkuDao()
		return skudao.update(sku)

