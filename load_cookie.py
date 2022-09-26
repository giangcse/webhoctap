import pickle
import json
from selenium import webdriver
from selenium.webdriver.common.by import By

# 0. Define browser
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--headless")
options.add_argument("--window-size=%s" % "1280,1024")

def _get_info_instagram(url):
    browser = webdriver.Chrome(executable_path = '/usr/lib/chromium-browser/chromedriver', chrome_options=options)

    cookies = pickle.load(open("my_cookie.pkl","rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)

    # 3. Refresh the browser
    browser.get(url)
    import time
    time.sleep(15)
    print(browser.title)
    uname = str(browser.title).split('@')[1]
    uname = uname.split(')')[0]
    url_pic = browser.find_element(By.CSS_SELECTOR, '[alt="'+str(uname)+'\'s profile picture"]').get_attribute('src')
    return json.loads(json.dumps({"uname": uname, "url_pic": url_pic}))
