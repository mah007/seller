from database.sku_dao import SkuDao
from database.user_dao import UserDao
from managers.user_manager import UserManager
from lazada_api.lazada_sku_api import LazadaSkuApi
from managers.response_helper import ResponseHelper


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

		# Validate certain size
		skudao = SkuDao()
		userdao = UserDao()
		addedSize = skudao.getAddedSize(user['id'])
		certainSize = userdao.getCertainSize(user['id'])
		if (addedSize >= certainSize):
			return ResponseHelper.generateErrorResponse("You cannot add more SKU!")

		# Validate SKU by lazada API
		lazadaSkuApi = LazadaSkuApi()
		lazadaProduct = lazadaSkuApi.getSku(sku, user)
		if not lazadaProduct:
			return ResponseHelper.generateErrorResponse("Can't access to Lazada service")

		# Add missing arguments and insert to our database
		sku['name'] = lazadaProduct['Attributes']['name'].encode('utf-8')
		sku['link'] = lazadaProduct['Skus'][0]['Url'].encode('utf-8')
		sku['special_price'] = lazadaProduct['Skus'][0]['special_price']

		skudao.insert(sku, user)
		return ResponseHelper.generateSuccessResponse(None)


	#-----------------------------------------------------------------------------
	# delete sku
	#-----------------------------------------------------------------------------
	def deleteSku(self, sku, token):
		user = self.validateToken(token)
		if 'error' in user:
			return user

		skudao = SkuDao()
		skudao.delete(sku)
		return ResponseHelper.generateSuccessResponse(None)


	#-----------------------------------------------------------------------------
	# get all skus
	#-----------------------------------------------------------------------------
	def getAll(self, token):
		user = self.validateToken(token)
		if 'error' in user:
			return user

		skudao = SkuDao()
		skus = skudao.getAll(user)
		return ResponseHelper.generateSuccessResponse(skus)


	#-----------------------------------------------------------------------------
	# Update sku state
	#-----------------------------------------------------------------------------
	def updateSkuState(self, sku, token):
		user = self.validateToken(token)
		if 'error' in user:
			return user

		skudao = SkuDao()
		skudao.updateState(sku)
		return ResponseHelper.generateSuccessResponse(None)


	#-----------------------------------------------------------------------------
	# update sku's info
	#-----------------------------------------------------------------------------
	def updateSku(self, sku, token):
		user = self.validateToken(token)
		if 'error' in user:
			return user

		skudao = SkuDao()
		skudao.update(sku)
		return ResponseHelper.generateSuccessResponse(None)











