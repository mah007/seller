import time
from utils.csv_utils import CSVUtils
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class CollectData:

  def performLogin(self, driver, account):
    print("---// Perform login")
    driver.get("https://sellercenter.lazada.vn/seller/login")
    # Enter email
    emailInput = driver.find_element_by_id("TPL_username")
    emailInput.clear()
    emailInput.send_keys(account['email'])
    # Enter password
    passwordInput = driver.find_element_by_id("TPL_password")
    passwordInput.clear()
    passwordInput.send_keys(account['password'])
    # click submit button
    loginButton = driver.find_element_by_class_name('la-login-form-item')
    loginButton.click()

  def clickNextButton(self, driver):
    driver.execute_script("document.getElementsByClassName('next-pagination-item')[8].click();")

  def gotopage(self, driver, page):
    gotopageInput = driver.find_element_by_xpath('//*[@id="_root"]/div/div[2]/div/div[4]/div[2]/span/input')
    gotopageInput.clear()
    gotopageInput.send_keys(page);
    gotopageButton = driver.find_element_by_xpath('//*[@id="_root"]/div/div[2]/div/div[4]/div[2]/button')
    gotopageButton.click()

  def performGetData(self, driver):
    rows = driver.find_elements_by_xpath('//*[@id="_root"]/div/div[2]/div/div[3]/div/div[2]/table/tbody/tr')
    for row in rows:
      email = row.find_elements_by_tag_name("td")[0].text
      name = row.find_elements_by_tag_name("td")[2].text
      api = row.find_elements_by_tag_name("td")[4].text
      row = [email, name, api]
      # From 0 -> 5410
      #CSVUtils.writeRow("./output/users_18_10_2017.csv", row)
      # From 5412  -> end
      CSVUtils.writeRow("./output/users_19_10_2017.csv", row)

  def performCollect(self, driver, account):
    wait = WebDriverWait(driver, 10)

    # Go to user page
    print('''---// Perform collect data''')
    driver.get("https://sellercenter.lazada.vn/seller/userManage")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".next-table-loading")))
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".next-table-loading")))
    # Go to current page
    self.gotopage(driver, "6671")
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".next-table-loading")))
    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".next-table-loading")))
    # Get next data
    for i in range(2244):
      self.performGetData(driver)
      self.clickNextButton(driver)
      wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".next-table-loading")))
      wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".next-table-loading")))

  def execute(self, driver, account):
    self.performLogin(driver, account)
    self.performCollect(driver, account)






