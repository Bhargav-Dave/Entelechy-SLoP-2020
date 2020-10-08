from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

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

# Extract all the articles from Each edition
def getEdition(driver,Edition):
    driver.get(Edition)
    Element = driver.find_elements_by_css_selector("article > h2 > a")
    articleLink = [Element.get_attribute('herf') for Element in Element]
    pages = driver.find_elements_by_css_selector(".page")
    




username = "" # Username
password = "" # Password
driver = Login(username,password)



driver.quit()