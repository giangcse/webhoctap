import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

# 0. Declare the browser
browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')

# 1. Open faceboook
browser.get("https://www.instagram.com")

# 2. Truy to login

sleep(20)

pickle.dump(browser.get_cookies(), open("insta.pkl","wb"))

browser.close()