import time
import operator
import requests
import threading
from time import sleep
from lxml import html
from database.sku_dao import SkuDao
from lazada_api.lazada_sku_api import LazadaSkuApi
from managers.auto_price_manager import AutoPriceManager


class AutoPriceWorker(threading.Thread):

	def __init__(self, kwargs):
		threading.Thread.__init__(self)
		self.kwargs = kwargs


	def run(self):
		user = self.kwargs['user']
		print('''*********** {}: is running ***********'''.format(user['lazada_user_name']))
		skudao = SkuDao()
		skus = skudao.getActiveSku(user)
		if (skus == None):
			return

		autoPriceManager = AutoPriceManager()
		for sku in skus:
			enemies = self.getEnemies(user, sku)
			self.priceAlgorithm(enemies, user, sku)
			autoPriceManager.insertHistory(sku, enemies, user)


	def priceAlgorithm(self, enemies, user, sku):
		newSpecialPrice = sku['special_price']
		if (enemies == None or len(enemies) <= 1):
			return

		# Get enemy have lowest price
		enemies = self.sortEnemies(enemies)
		lowestPriceEnemy = enemies[0]
		lowSecondPriceEnemy = enemies[1]

		# Our product price will be lower then enemy compete_price unit
		newSpecialPrice = lowestPriceEnemy['price'] - sku['compete_price']
		if (user['lazada_user_name'].lower() == lowestPriceEnemy['name'].lower()):
			newSpecialPrice = lowSecondPriceEnemy['price'] - sku['compete_price']

		# But this is not lower then min_price and higher then max_price
		if (newSpecialPrice < sku['min_price']):
			newSpecialPrice = sku['min_price']
		if (newSpecialPrice > sku['max_price']):
			newSpecialPrice = sku['max_price']

		if (sku['special_price'] == newSpecialPrice):
			return

		self.doUpdatePrice(sku, user, newSpecialPrice)


	def doUpdatePrice(self, sku, user, newSpecialPrice):
		sku['updated_at'] = int(round(time.time()))
		sku['special_price'] = newSpecialPrice
		# Update internal database
		skuDao = SkuDao()
		skuDao.updateSpecialPrice(sku)
		# Update external database
		lazadaSkuApi = LazadaSkuApi()
		lazadaProduct = lazadaSkuApi.updateProductSpecialPrice(sku, user, newSpecialPrice)
		print ('''{} ({}): updated price to: {}'''.format(sku['sku'], user['lazada_user_name'], newSpecialPrice))


	def getEnemies(self, user, sku):
		enemiesJson = []
		page = requests.get(sku['link'])
		tree = html.fromstring(page.content)

		# Top enemy, will be this user if the user is on the top
		topEnemyPrice = tree.xpath('//*[@id="special_price_box"]/text()')
		topEnemyName = tree.xpath('//*[@id="prod_content_wrapper"]/div[2]/div[2]/div[1]/div[1]/a/text()')
		topEnemyJson = {
			"name": topEnemyName[0].replace(' ',''),
			"price": int(topEnemyPrice[0].replace('VND', '').replace('.', '').replace(',', ''))
		}
		enemiesJson.append(topEnemyJson)

		# List others enemy
		enemies = tree.xpath('//*[@id="multisource"]/div[2]/table/tr[2]/td[1]/div/div/a/span/text()')
		enemyPrices = tree.xpath('//*[@id="multisource"]/div[2]/table/tr[2]/td[4]/span/text()')
		for index, enemy in enumerate(enemies):
			enemiesJson.append({
				"name": enemy.replace(' ',''),
				"price": int(enemyPrices[index].replace('VND', '').replace('.', ''))
				})

		print ('''{} ({}) enemies: {}'''.format(sku['sku'], user['lazada_user_name'], enemiesJson))
		return enemiesJson


	def sortEnemies(self, enemies):
		return sorted(enemies, key=operator.itemgetter('price'))




