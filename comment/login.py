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
		email.send_keys("info@lazada.com")

		password.clear()
		password.send_keys("lakamipassword")

		loginButton.click()

	def tearDown(self):
		print("Login Success")

if __name__ == '__main__':
	unittest.main()

