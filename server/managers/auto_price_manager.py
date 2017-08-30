from database.sku_dao import SkuDao
from database.user_dao import UserDao
from database.history_dao import HistoryDao
from managers.user_manager import UserManager
from lazada_api.lazada_sku_api import LazadaSkuApi
from managers.response_helper import ResponseHelper
import time
from time import sleep
from lxml import html
import requests
import json

class AutoPriceManager(object):

	def initialize(self):
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
	# INSERT NEW HISTORY
	#-----------------------------------------------------------------------------
	def insertHistory(self, sku, enemies, user):
		historyDao = HistoryDao()
		i = 1
		enemyJson = ""
		historyDao.deleteHistory(sku)

		for enemy in enemies:
			enemyJson = enemyJson + str(enemy['name']) + ' - ' + str(enemy['price']) + "\n"
			if(i > 5):
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


