from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Comment:

	def give_rating(self, driver, rating):
		if (rating == 4):
			star = driver.find_elements_by_xpath('//*[@id="ProductRatingForm"]/div[1]/div[1]/div/label[2]')
			star.click()
		else: # Default is 5 star
			star = driver.find_elements_by_xpath('//*[@id="ProductRatingForm"]/div[1]/div[1]/div/label[1]')
			star.click()

	def enter_title(self, driver, title):
		titleInput = driver.find_elements_by_xpath('//*[@id="RatingForm_title"]')
		titleInput.clear()
		titleInput.send_keys(title)

	def enter_comment(self, driver, comment):
		titleInput = driver.find_elements_by_xpath('//*[@id="RatingForm_title"]')
		titleInput.clear()
		titleInput.send_keys(comment)

	def click_submit_button(self, driver):
		submitButton = driver.find_elements_by_xpath('//*[@id="ProductRatingFormAction"]/div/input')
		submitButton.click()

	def giveComment(self, driver, product, comment):
		print('''---// {} give comment for {} '''.format(account['email'], product['site']))

		try:
			driver.get(product['site'])

			# Click this button to see feedback form
			# give_feedback_button = driver.find_elements_by_xpath('//*[@id="productReview"]/div[1]/header/span')
			# give_feedback_button.click()

			self.give_rating(driver, comment['rating'])
			self.enter_title(driver, comment['title'])
			self.enter_comment(driver, comment['comment'])
			self.click_submit_button(driver)

			resultContent = driver.find_element_by_class_name('c-review-form__pending')
			result = resultContent.find_element_by_class_name('c-review-pending__message') # If success there will be have a review message
			if result is not None:
				print('''---// Give comment result {} '''.format(result.text))

			return result
		except Exception as ex:
			print('''---// Comment got exception: {} '''.format(ex))
			return ex






