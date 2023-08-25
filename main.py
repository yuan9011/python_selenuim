import time
from selenium import webdriver

url = 'https://www.google.com/'
driver = webdriver.Chrome()
driver.get(url)
time.sleep(10)
driver.quit()