from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Login:

	def enter_email(self, driver, email):
		emailInput = driver.find_element_by_id("LoginForm_email")
		emailInput.clear()
		emailInput.send_keys(email)

	def enter_password(self, driver, password):
		passwordInput = driver.find_element_by_id("LoginForm_password")
		passwordInput.clear()
		passwordInput.send_keys(password)

	def click_login_button(self, driver):
		loginButton = driver.find_element_by_class_name('ui-buttonCta')
		driver.execute_script("$(arguments[0]).click();", loginButton)

	def performLogin(self, driver, account):
		print('''---// Login with account: {} '''.format(account['email']))
		driver.get("https://www.lazada.vn/customer/account/login")

		try:
			self.enter_email(driver, account['email'])
			self.enter_password(driver, account['password'])
			self.click_login_button(driver);
		except Exception as ex:
			print('''---// Login got exception: {} '''.format(ex))
			return ex

		try:
			result = driver.find_element_by_class_name("s-error")
			if result is not None:
				print('''---// Login failed: {} '''.format(result.text))

			return result
		except Exception as ex: # If succes exception will happen because cannot find class s-error
			return None 	        # Marked as success




