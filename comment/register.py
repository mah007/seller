from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import time
import urllib
import requests

def click_register(driver):
    back_button = driver.find_element_by_xpath("/html/body/div[1]/div/div/header/div[1]/nav/ul/li[6]/a")
    back_button.click()

def enter_email(driver, email):
    input_field = driver.find_element_by_id("RegistrationForm_email")
    input_field.send_keys(email)

def enter_name(driver, usernam):
    input_field = driver.find_element_by_id("RegistrationForm_first_name")
    input_field.send_keys(usernam)

def enter_password(driver, password):
    input_field = driver.find_element_by_id("RegistrationForm_password")
    input_field.send_keys(password)

def enter_repassword(driver, password):
    input_field = driver.find_element_by_id("RegistrationForm_password2")
    input_field.send_keys(password)

def click_register_button(driver):
    back_button = driver.find_element_by_id("send")
    back_button.click()

def performRegister(driver):
    driver.set_window_position(0, 0)
    driver.set_window_size(720, 1100)

    print("---// Open Lazada.vn ")
    driver.get("https://www.lazada.vn")
    print("---// Go to register page")
    click_register(driver)

    print("---// Enter email")
    enter_email(driver, "afsdfagsghrthtrye@gmail.com")
    print("---// Enter name")
    enter_name(driver, "Nguyen Thanh Tuan")
    print("---// Enter password")
    enter_password(driver, "a111333999")
    print("---// Enter repassword")
    enter_repassword(driver, "a111333999")
    print("---// Click register")
    click_register_button(driver);

    driver.quit()

if __name__ == "__main__":
    driver = webdriver.Chrome()
    performRegister(driver)




