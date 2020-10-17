from selenium import webdriver
from selenium.webdriver.firefox.options import Options

url = "http://entelechy.daiict.ac.in"

# Intialized web Browser
def initBrowser():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    return driver

# Connecting and login
def Login(username,password):
    driver = initBrowser()
    driver.get(url)
    driver.find_element_by_id("user_login").send_keys(username)
    driver.find_element_by_id("user_pass").send_keys(password)
    driver.find_element_by_id("wp-submit").click()
    return driver

