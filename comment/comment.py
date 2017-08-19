import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Comment:

	def click_give_feedback_button(self, driver):
		showFeedbackButton = driver.find_element_by_class_name('c-review-form__button_name_write-review')
		showFeedbackButton.click()

	def give_rating(self, driver, rating):
		if (rating == 4):
			star = driver.find_element_by_id('ratingStarsItem-4')
			driver.execute_script("$(arguments[0]).click();", star)
		else: # Default is 5 star
			star = driver.find_element_by_id('ratingStarsItem-5')
			driver.execute_script("$(arguments[0]).click();", star)

	def enter_title(self, driver, title):
		titleInput = driver.find_element_by_class_name('c-review-form__input-text_name_title')
		titleInput.clear()
		titleInput.send_keys(title)

	def enter_comment(self, driver, comment):
		titleInput = driver.find_element_by_class_name('c-review-form__input-text_name_comment')
		titleInput.clear()
		titleInput.send_keys(comment)

	def click_submit_button(self, driver):
		submitButton = driver.find_element_by_class_name('c-review-form__button_name_submit')
		submitButton.click()

	def giveComment(self, driver, account, product, comment):
		print('''---// {} give comment ==> {} for {} '''.format(account['email'], comment['comment'], product['site']))

		try:
			driver.get(product['site'])
			self.click_give_feedback_button(driver)
			self.give_rating(driver, comment['rating'])
			self.enter_title(driver, comment['title'])
			self.enter_comment(driver, comment['comment'])
			self.click_submit_button(driver)
		except Exception as ex:
			print('''---// Give comment got exception: {} '''.format(ex))
			return ex

		try:
			time.sleep(1)
			result = driver.find_element_by_class_name('c-review-pending__message')
			return None # If success there will be have a review message
		except Exception as ex:
			print('''---// Give comment is error: {} '''.format(ex))
			return ex






