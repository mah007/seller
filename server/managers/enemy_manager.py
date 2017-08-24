from database.sku_dao import SkuDao
from database.user_dao import UserDao
from database.enemy_dao import EnemyDao
from managers.user_manager import UserManager
from lazada_api.lazada_sku_api import LazadaSkuApi
from managers.response_helper import ResponseHelper
from runners.price_automatically_worker import PriceAutomaticallyWorker
import time
from time import sleep
from lxml import html
import requests
import json

class EnemyManager(object):

	def initialize(self):
		enemyDao = EnemyDao()
		enemyDao.createTable()


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
	def insertEnemy(self, sku, enemy_json):
		enemyDao = EnemyDao()
		enemyDao.insert(sku, enemy_json)
		return ResponseHelper.generateSuccessResponse(None)

	#-----------------------------------------------------------------------------
	# GET ALL ENEMIES IN DATABASE
	#-----------------------------------------------------------------------------
	def getEnemy(self, user, token):
		user = self.validateToken(token)
		enemyDao = EnemyDao()
		if 'error' in user:
			return user

		enemies = self.run(user)
		result = enemyDao.getEnemy()

		return ResponseHelper.generateSuccessResponse(result)

	def run(self, user):
		skudao = SkuDao()
		enemyDao = EnemyDao()
		skus = skudao.getActiveSku(user)
		if (skus == None):
			return
		enemyDao.deleteEnemyBeforeInsert()

		for sku in skus:
			enemies = self.getEnemies(sku)
			enemyDao.insert(sku, enemies)

	def getEnemies(self, sku):
		enemiesJson = []
		page = requests.get(sku['link'])
		tree = html.fromstring(page.content)

		# Top enemy, will be this user if the user is on the top
		topEnemyPrice = tree.xpath('//*[@id="special_price_box"]/text()')
		topEnemyName = tree.xpath('//*[@id="prod_content_wrapper"]/div[2]/div[2]/div[1]/div[1]/a/text()')
		topEnemyJson = topEnemyName[0] + ' - ' + str(int(topEnemyPrice[0].replace('.', '').replace(',', '')))

		# List others enemy
		enemies = tree.xpath('//*[@id="multisource"]/div[2]/table/tr[2]/td[1]/div/div/a/span/text()')
		enemyPrices = tree.xpath('//*[@id="multisource"]/div[2]/table/tr[2]/td[4]/span/text()')

		result = topEnemyJson
		count = 0

		for index, enemy in enumerate(enemies):
			result = result + ', ' + enemy.replace('\n', ' ').replace('\r', '').replace('\t','').replace(' ','') + " - " + str((int(enemyPrices[index].replace('VND', '').replace('.', '').replace('\t','').replace(' ',''))))
			result.replace('\t','')
			count = count + 1
			if (count > 5):
				return result

		return result