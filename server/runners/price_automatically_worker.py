import requests
from time import sleep
from lxml import html
from database.sku_dao import SkuDao
from database.user_dao import UserDao
from lazada_api.lazada_sku_api import LazadaSkuApi


class PriceAutomaticallyWorker(object):

	def execute(self):
		print("*********** Price Automatically is executed ***********")
		skudao = SkuDao()
		skus = skudao.getAll()
		if (skus == None):
			return

		for sku in skus:
			enemies = self.getEnemies(sku['link'])
			newSpecialPrice = self.priceAlgorithm(enemies, sku)
			self.doUpdatePrice(sku, newSpecialPrice)


	def priceAlgorithm(self, enemies, sku):
		newSpecialPrice = sku['special_price']
		if (enemies == None):
			return newSpecialPrice

		# Get enemy have lowest price
		lowestPriceEnemy = enemies[0]
		for enemy in enemies:
			if (enemy['price'] < lowestPriceEnemy['price']):
				lowestPriceEnemy = enemy
		
		# Our product price will be lower then enemy compete_price unit
		newSpecialPrice = lowestPriceEnemy['price'] - sku['compete_price']

		# But this is not lower then min_price and higher then max_price
		if (newSpecialPrice < sku['min_price']):
			newSpecialPrice = sku['min_price']
		if (newSpecialPrice > sku['max_price']):
			newSpecialPrice = sku['max_price']

		print (newSpecialPrice)
		return newSpecialPrice


	def doUpdatePrice(self, sku, newSpecialPrice):
		if (sku == None or sku['special_price'] == newSpecialPrice):
			return

		userDao = UserDao()
		temporaryUser = userDao.getUser("token");
		lazadaSkuApi = LazadaSkuApi()
		lazadaProduct = lazadaSkuApi.updateProductSpecialPrice(sku, temporaryUser, newSpecialPrice)
		print("*********** Price Automatically do updated price ***********")
		print("Sku: ", sku['sku'], "/nnew special price: ", newSpecialPrice)


	def getEnemies(self, pageUrl):
		page = requests.get(pageUrl)
		tree = html.fromstring(page.content)
		enemies = tree.xpath('//*[@id="multisource"]/div[2]/table/tr[2]/td[1]/div/div/a/span/text()')
		enemyPrices = tree.xpath('//*[@id="multisource"]/div[2]/table/tr[2]/td[4]/span/text()')

		enemiesJson = []
		for index, enemy in enumerate(enemies):
			enemiesJson.append({
				"name": enemy,
				"price": int(enemyPrices[index].replace('VND', '').replace('.', ''))
				})

		print(enemiesJson)
		return enemiesJson





