import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import randint


class IncreaseView:

    def scroll_down(self, driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    def scroll_up(self, driver):
        driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
        time.sleep(3)

    def add_to_cart(self, driver):
        submitButton = driver.find_element_by_id('AddToCart')
        submitButton.click()
        time.sleep(3)

    def close_popup(self, driver):
        submitButton = driver.find_element_by_class_name('nyroModalClose nyroModalCloseButton nmReposition')
        submitButton.click()

    def order_product(self, driver):
        submitButton = driver.find_element_by_class_name('btn-checkout col submit_btn mtssel-cart-checkout-button')
        submitButton.click()
    
    def how_to_buy(self, driver):
        submitButton = driver.find_element_by_class_name('txt-howtobuy')
        submitButton.click()    

    def go_to_store(self, driver):
        submitButton = driver.find_element_by_xpath("//*[@id='prod_content_wrapper']/div[2]/div[3]/div[3]/a")
        submitButton.click()

    def click_like(self, driver):
        submitButton = driver.find_element_by_xpath("//*[@id='prodinfo']/div[1]/div/div[2]/div[1]/div/div/span[1]")
        submitButton.click()

    # Multiple action to do in page
    def action_order_complete(self, driver):
        self.add_to_cart(driver)
        self.order_product(driver)

    def action_order_non_complete(self, driver):
        self.add_to_cart(driver)
        self.close_popup(driver)

    def performIncrease(self, driver, account, product):
        try:
            driver.get(product['site'])
            time.sleep(3)
            self.scroll_down(driver)
            self.scroll_up(driver)
            self.click_like(driver)
            
            random = randint(0,5)
            print(random)
            if random == 0:
                self.action_order_complete(driver)
            elif random == 1:
                self.action_order_non_complete(driver)
            elif random == 2:
                self.how_to_buy(driver)
            elif random == 3:
                self.action_order_complete(driver)
            elif random == 4:
                self.action_order_non_complete(driver)
            elif random == 5:
                self.click_like(driver)

            

        except Exception as ex:
            print('''---// Increasing view got exception: {} '''.format(ex))
            return ex

        try:
            time.sleep(1)
            result = driver.find_element_by_class_name('c-review-pending__message')
            print('''---// {} Increasing view  ==> {} ==> {} '''.format(account['email'], roduct['site']))
            return None # If success there will be have a review message
        except Exception as ex:
            print('''---// Increasing view is error: {} '''.format(ex))
            return ex

