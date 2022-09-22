from lib2to3.pgen2 import driver
from operator import indexOf
import profile
from selenium import webdriver

driver = webdriver.Chrome(executable_path='chromedriver.exe')

driver.get('https://www.tiktok.com/@nguyenhanh0980')

profile_picture = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[1]/span/img').get_attribute("src")
title = driver.title
user_name = str(title)[:str(title).index("TikTok")]
print(user_name, profile_picture)
driver.quit()