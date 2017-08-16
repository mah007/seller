from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest

# firefox_capabilities = DesiredCapabilities.FIREFOX
# firefox_capabilities['marionette'] = True
# firefox_capabilities['binary'] = '/usr/bin/firefox'

class LoginTest(unittest.TestCase):

	def setUp(self):

		self.driver = webdriver.Firefox()
		self.driver.get("https://www.lazada.vn/customer/account/login/")


	def test_Login(self):
		driver = self.driver
		email = driver.find_element_by_id("LoginForm_email")
		password = driver.find_element_by_id("LoginForm_password")
		loginButton = driver.find_element_by_class_name("ui-buttonCta")

		email.clear()
		email.send_keys("lzdseller@gmail.com")

		password.clear()
		password.send_keys("Hoangbeatb3")

		loginButton.click()

		div = self.driver.find_element_by_class_name('logo')
		href = div.find_element_by_css_selector('a')

		href.click()

		driver.get('https://www.lazada.vn/apple-iphone-7-32gb-hong-hang-nhap-khau-7629048.html?spm=a2o4n.home.sku-feed-slider-with-banner_452505.12.1cFAdR')		

		div = self.driver.find_element_by_class_name('c-input-group__input-wrap')
		textArea = div.find_element_by_css_selector('textarea')
		commentText = "This is a good devices!"
		textArea.clear()
		textArea.send_keys(commentText)		

		div = driver.find_element_by_class_name('c-input-group__button-container')
		questionButton = div.find_element_by_css_selector('button')
		questionButton.click()		




	def tearDown(self):
		print("Login Success")

if __name__ == '__main__':
	unittest.main()

