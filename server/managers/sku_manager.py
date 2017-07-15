from database.sku_dao import SkuDao
from database.user_dao import UserDao
from managers.user_manager import UserManager
from lazada_api.lazada_sku_api import LazadaSkuApi
from managers.response_helper import ResponseHelper


ERROR = {"error": ""}
SUCCESS = {"success": "done"}


class SkuManager(object):

	def initialize(self):
		skudao = SkuDao()
		skudao.createTable()


	def validateToken(self, token):
		userDao = UserDao()
		user = userDao.getUser(token)
		if user == None:
			return ResponseHelper.generateErrorResponse("Invalid token")
		else:
			return user


	#-----------------------------------------------------------------------------
	# insert new sku
	#-----------------------------------------------------------------------------
	def insertSku(self, sku, token):
		user = self.validateToken(token)
		if 'error' in user:
			return user

		# Validate SKU by lazada API
		lazadaSkuApi = LazadaSkuApi()
		lazadaProduct = lazadaSkuApi.getSku(sku, user)
		if not lazadaProduct:
			return ResponseHelper.generateErrorResponse("Can't access to Lazada service")

		# Add missing arguments and insert to our database
		sku['name'] = lazadaProduct['Attributes']['name'].encode('utf-8')
		sku['link'] = lazadaProduct['Skus'][0]['Url'].encode('utf-8')
		sku['special_price'] = lazadaProduct['Skus'][0]['special_price']
		skudao = SkuDao()
		skudao.insert(sku, user)
		return ResponseHelper.generateSuccessResponse(None)


	def deleteSku(self, sku, token):
		user = self.validateToken(token)
		if 'error' in user:
			return user

		skudao = SkuDao()
		skudao.delete(sku)
		return SUCCESS


	def getAll(self, token):
		user = self.validateToken(token)
		if 'error' in user:
			return user

		skudao = SkuDao()
		skus = skudao.getAll(user)
		return ResponseHelper.generateSuccessResponse(skus)


	def updateSkuState(self, sku, token):
		user = self.validateToken(token)
		if 'error' in user:
			return user

		skudao = SkuDao()
		skudao.updateState(sku)
		return SUCCESS


	def updateSku(self, sku, token):
		user = self.validateToken(token)
		if 'error' in user:
			return user

		skudao = SkuDao()
		skudao.update(sku)
		return SUCCESS











