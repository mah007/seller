import time
import requests
import json
from time import sleep
from lxml import html
from database.price_balancer import PriceBalancerDao
from database.user_dao import UserDao
from managers.user_manager import UserManager
from lazada_api.lazada_sku_api import LazadaSkuApi
from managers.response_helper import ResponseHelper
from utils.response_utils import ResponseUtils
from database.history_dao import HistoryDao
from config import SkuHistoryConfig
from utils.timestamp_utils import TimestampUtils


class PriceBalancerManager(object):

	def initialize(self):
		priceBalancer = PriceBalancerDao()
		priceBalancer.createTable()

	def validateToken(self, token):
		userDao = UserDao()
		user = userDao.getUser(token)
		if user == None:
			return ResponseHelper.generateErrorResponse("Invalid token")
		else:
			return user


	# ----------------------------------------------------------------------------
	# Insert price balancer
	# ----------------------------------------------------------------------------
	def insert(self, pb, token):
		userToken = self.validateToken(token)
		if 'error' in userToken:
			return userToken

		priceBalancerDao = PriceBalancerDao()
		result = priceBalancerDao.insert(pb)
		if 'success' in result:
			return ResponseHelper.generateSuccessResponse(None)
		return ResponseHelper.generateErrorResponse("Unable to insert new Price Balancer")











