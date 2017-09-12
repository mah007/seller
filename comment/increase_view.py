import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class IncreaseView:

	def scroll_down(self, driver):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(SCROLL_PAUSE_TIME)

	def scroll_up(self, driver):
		driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
		time.sleep(SCROLL_PAUSE_TIME)

	def add_to_cart(self, driver):
		submitButton = driver.find_element_by_id('AddToCart')
		submitButton.click()

	def close_popup(self, driver):
		submitButton = driver.find_element_by_class_name('nyroModalClose nyroModalCloseButton nmReposition')
		submitButton.click()

	def order_product(self, driver):
		submitButton = driver.find_element_by_class_name('btn-checkout col submit_btn mtssel-cart-checkout-button')
		submitButton.click()

	def performIncrease(self, driver, account, product):
		try:
			driver.get(product['site'])
			time.sleep(3)
			self.scroll_down(driver)
			self.scroll_up(driver)
		except Exception as ex:
			print('''---// Give comment got exception: {} '''.format(ex))
			return ex

		try:
			time.sleep(1)
			result = driver.find_element_by_class_name('c-review-pending__message')
			print('''---// {} give comment ==> {} ==> {} '''.format(account['email'], comment['title'], product['site']))
			return None # If success there will be have a review message
		except Exception as ex:
			print('''---// Give comment is error: {} '''.format(ex))
			return ex






