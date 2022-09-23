import telebot
import random
import json
import sqlite3
import validators
import requests

from selenium import webdriver
from bs4 import BeautifulSoup

class Via_Telegram:
    def __init__(self) -> None:
        # Khởi tạo thông tin bot
        self.bot_token = '5422598877:AAFL08R_G8TUVoej8jAYREkQ9uKQrg6jiqs'
        self.bot = telebot.TeleBot(token=self.bot_token, parse_mode='HTML')
        # Handle message /add
        @self.bot.message_handler(commands=["add"])
        def add_info(message):
            self._add_info(message)
        # Khởi tạo thông tin kết nối đến Database
        self.database = 'data.db'
        self.connection_db = sqlite3.connect(self.database, check_same_thread=False)
        self.cursor = self.connection_db.cursor()
        # Chrome driver
        # self.driver = webdriver.Chrome(executable_path='chromedriver.exe')
        self.driver = webdriver.Chrome(executable_path = '/usr/lib/chromium-browser/chromedriver')

    # Get dữ liệu từ Instagram
    def _get_info_instagram(self, url_instagram, contributor):
        headersList = {
            "Accept": "*/*",
        }
        payload = ""
        try:
            response = requests.request("GET", url_instagram, data=payload,  headers=headersList)
            # print(response.text)
            data = BeautifulSoup(response.text, "html5lib")
            info = str(data.title).split('•')[0][7:]

            idx = (str(data).index('"profile_pic_url":'))
            url_pic = (str(data)[idx+19:idx+500].split('"')[0].replace('\\', ''))

            self.cursor.execute('INSERT OR IGNORE INTO main (URL, USERNAME, URL_PIC, CONTRIBUTORS) VALUES(?, ?, ?, ?)', (url_instagram, info.strip(), url_pic, contributor))
            self.connection_db.commit()
            return 1
        except Exception as e:
            return 0

    # Get dữ liệu từ Tiktok
    def _get_info_tiktok(self, url_tiktok, contributor):
        try:
            self.driver.get(url_tiktok)
            profile_picture = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div/div[1]/div[1]/div[1]/span/img').get_attribute("src")
            title = self.driver.title
            user_name = str(title)[:str(title).index("TikTok")]
            
            self.cursor.execute('INSERT OR IGNORE INTO main (URL, USERNAME, URL_PIC, CONTRIBUTORS) VALUES(?, ?, ?, ?)', (url_tiktok, user_name.strip(), profile_picture, contributor))
            self.connection_db.commit()
            self.driver.quit()
            return 1
        except Exception as e:
            return 0

    # Thêm mới dữ liệu
    def _add_info(self, message):
        if('/add' in str(message.text).lower()):
            try:
                url = str(message.text).split(' ')[1]
                contributor = str(message.from_user.username)
                if(validators.url(url)):
                    if('instagram' in str(url).lower()):
                        self._get_info_instagram(url, contributor)
                        self.bot.reply_to(message, "🌟<b>XIN CHÂN THÀNH CẢM ƠN SỰ ĐÓNG GÓP CỦA BẠN</b>🌟\nCảm ơn sự đóng góp của bạn làm cho cộng đồng ngày càng phát triển, đời sống của anh em được cải thiện.\nXin vinh danh sự đóng góp này, bravo!!!")
                    elif('tiktok' in str(url).lower()):
                        self._get_info_tiktok(url, contributor)
                        self.bot.reply_to(message, "🌟<b>XIN CHÂN THÀNH CẢM ƠN SỰ ĐÓNG GÓP CỦA BẠN</b>🌟\nCảm ơn sự đóng góp của bạn làm cho cộng đồng ngày càng phát triển, đời sống của anh em được cải thiện.\nXin vinh danh sự đóng góp này, bravo!!!")
                    else:
                        self.bot.reply_to(message, '<i>Hiện tại hệ thống chưa hỗ trợ trang web này. Cảm ơn vì sự đóng góp của bạn!</i>')
            except Exception as e:
                self.bot.reply_to(message, 'Vui lòng điền URL hợp lệ!')

if __name__ == '__main__':
    via_tele = Via_Telegram()
    via_tele.bot.infinity_polling()
