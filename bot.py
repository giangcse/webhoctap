import telebot
import random
import json
import sqlite3
import validators
import requests

from selenium import webdriver
from bs4 import BeautifulSoup

# Bot telegram config
token = '5422598877:AAFL08R_G8TUVoej8jAYREkQ9uKQrg6jiqs'
chat_id = -772415172
bot = telebot.TeleBot(token, parse_mode="html")
# SQLite3 Config
conn = sqlite3.connect('tailieuhoctap.db')
cursor = conn.cursor()

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if('/otp' in message.text):
        OTP = random.randint(1000, 9999)
        with open('otp.json', 'w') as f:
            f.write(json.dumps({"otp": OTP}, indent=4))
        bot.reply_to(message, '<b>OTP Tài liệu học tập</b>\nMã OTP: <pre>'+str(OTP)+'</pre>')
    if('/add' in message.text):
        url = str(message.text).split(' ')[1]
        if(validators.url(url)):
            reqUrl = "http://127.0.0.1:88/add?url=" + url

            headersList = {
            "Accept": "*/*",
            "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
            }

            payload = ""
            response = requests.request("GET", reqUrl, data=payload,  headers=headersList)


            # if('instagram' in str(url)):
            #     getInfoUser_instagram(url)
            #     bot.reply_to(message, '<b>🥇 TRAO TẶNG HUÂN CHƯƠNG CỐNG HIẾN</b>\nToàn thể anh em xin chân thành cảm ơn ' + message.from_user.first_name + ' vì đã có những đóng góp to lớn cho cộng đồng.')
            # elif('tiktok' in str(url)):
            #     getInfoUser_tiktok(url)
            bot.reply_to(message, '<b>🥇 TRAO TẶNG HUÂN CHƯƠNG CỐNG HIẾN</b>\nToàn thể anh em xin chân thành cảm ơn ' + message.from_user.first_name + ' vì đã có những đóng góp to lớn cho cộng đồng.')
        else:
            bot.reply_to(message, '<i>URL không hợp lệ, vui lòng kiểm tra lại</b>')


def getInfoUser_tiktok(url_profile):
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    try:
        driver.get(url_profile)
        profile_picture = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[1]/span/img').get_attribute("src")
        title = driver.title
        user_name = str(title)[:str(title).index("TikTok")]
        # print(user_name, profile_picture)
        cursor.execute('INSERT OR IGNORE INTO data VALUES("'+str(user_name)+'", "'+str(profile_picture)+'", "'+str(url_profile)+'")')
        conn.commit()
        driver.quit()
    except Exception as e:
        return e

def getInfoUser_instagram(url_profile):
    headersList = {
        "Accept": "*/*",
    }
    payload = ""
    try:
        response = requests.request("GET", url_profile, data=payload,  headers=headersList)

        data = BeautifulSoup(response.text, "html")
        info = str(data.title).split('•')[0][7:]

        idx = (str(data).index('"profile_pic_url":'))
        url_pic = (str(data)[idx+19:idx+500].split('"')[0].replace('\\', ''))

        cursor.execute('INSERT OR IGNORE INTO data VALUES("'+str(info)+'", "'+str(url_pic)+'", "'+str(url_profile)+'")')
        conn.commit()
    except Exception as e:
        return e


if __name__=='__main__':
    bot.infinity_polling()