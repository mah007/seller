from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Register:

    def enter_email(self, driver, email):
        input_field = driver.find_element_by_id("RegistrationForm_email")
        input_field.clear()
        input_field.send_keys(email)

    def enter_name(self, driver, name):
        input_field = driver.find_element_by_id("RegistrationForm_first_name")
        input_field.clear()
        input_field.send_keys(name)

    def enter_password(self, driver, password):
        input_field = driver.find_element_by_id("RegistrationForm_password")
        input_field.clear()
        input_field.send_keys(password)

    def enter_repassword(self, driver, password):
        input_field = driver.find_element_by_id("RegistrationForm_password2")
        input_field.clear()
        input_field.send_keys(password)

    def click_register_button(self, driver):
        register_button = driver.find_element_by_id("send")
        register_button.click()

    def performRegister(self, driver, account):
        print('''---// Register with account: {} '''.format(account['email']))
        driver.get("https://www.lazada.vn/customer/account/create")

        try:
            self.enter_email(driver, account['email'])
            self.enter_name(driver, account['name'])
            self.enter_password(driver, account['password'])
            self.enter_repassword(driver, account['password'])
            self.click_register_button(driver);
        except Exception as ex:
            print('''---// Register got exception: {} '''.format(ex))
            return ex

        try:
            result = driver.find_element_by_class_name("s-error")
            if result is not None:
                print('''---// Register failed: {} '''.format(result.text))

            return result
        except Exception as ex: # If succes exception will happen because cannot find class s-error
            return None         # Marked as success





