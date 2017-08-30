from database.sku_dao import SkuDao
from database.user_dao import UserDao
from managers.user_manager import UserManager
from lazada_api.lazada_sku_api import LazadaSkuApi
from managers.response_helper import ResponseHelper
from utils.response_utils import ResponseUtils
from database.history_dao import HistoryDao
from config import SkuHistoryConfig
import time
from time import sleep
from lxml import html
import requests
import json


class SkuManager(object):

	def initialize(self):
		skudao = SkuDao()
		skudao.createTable()
		historyDao = HistoryDao()
		historyDao.createTable()


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
		checkExistSku = skudao.checkExistSku(sku)
		if (checkExistSku > 0):
			return ResponseUtils.generateErrorResponse("You cannot add SKU already exist!!!")

		addedSize = skudao.getAddedSize(user['id'])
		certainSize = userdao.getCertainSize(user['id'])
		if (addedSize >= certainSize):
			return ResponseUtils.generateErrorResponse("You cannot add more SKU, please contact admin to improve your account!")

		# Validate SKU by lazada API
		lazadaSkuApi = LazadaSkuApi()
		lazadaProduct = lazadaSkuApi.getSku(sku, user)
		if 'error' in lazadaProduct:
			return ResponseUtils.generateErrorResponse(lazadaProduct['error'])

		# Add missing arguments and insert to our database
		sku['name'] = lazadaProduct['Attributes']['name'].encode('utf-8')
		sku['link'] = lazadaProduct['Skus'][0]['Url'].encode('utf-8')
		sku['special_price'] = lazadaProduct['Skus'][0]['special_price']

		skudao.insert(sku, user)
		return ResponseUtils.generateSuccessResponse()


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

	#-----------------------------------------------------------------------------
	# INSERT NEW HISTORY
	#-----------------------------------------------------------------------------
	def insertHistory(self, sku, enemies, user):
		historyDao = HistoryDao()
		i = 1
		enemyJson = ""
		historyDao.deleteHistory(sku)

		for enemy in enemies:
			enemyJson = enemyJson + str(enemy['name']) + ' - ' + str(enemy['price']) + "\n"
			if(i > SkuHistoryConfig.HISTORY_SIZE):
				historyDao.insertHistory(sku, enemyJson, user)
				return ResponseHelper.generateSuccessResponse(None)
			i = i + 1

		historyDao.insertHistory(sku, enemyJson, user)

		return ResponseHelper.generateSuccessResponse(None)

	#-----------------------------------------------------------------------------
	# GET ALL ENEMIES IN DATABASE
	#-----------------------------------------------------------------------------
	def getAllHistory(self, token):
		user = self.validateToken(token)
		historyDao = HistoryDao()
		if 'error' in user:
			return user

		result = historyDao.getAllHistory(user)

		return ResponseHelper.generateSuccessResponse(result)











