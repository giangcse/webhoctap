import pickle
import telebot
import random
import json
import sqlite3
import validators
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
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
        # Handle message /rank
        @self.bot.message_handler(commands=["rank"])
        def rank(message):
            rank_users = self._rank_user(message)
            content = '<b>🎖 DANH SÁCH ĐÓNG GÓP 🎖</b>\n'
            ranks = ['🥇', '🥈', '🥉']
            i = 1
            for u in rank_users:
                if(i==1):
                    content += str(ranks[0]) + '  @' + u['contributor'] + ' với ' + str(u['amount']) + ' đóng góp.\n'
                elif(i==2):
                    content += str(ranks[1]) + '  @' + u['contributor'] + ' với ' + str(u['amount']) + ' đóng góp.\n'
                elif(i==3):
                    content += str(ranks[2]) + '  @' + u['contributor'] + ' với ' + str(u['amount']) + ' đóng góp.\n'
                else:
                    content += str(i) + '  @' + u['contributor'] + ' với ' + str(u['amount']) + ' đóng góp.\n'
                i+=1
            self.bot.reply_to(message, content)
        #Handle message /remove
        @self.bot.message_handler(commands=["remove"])
        def remove_info(message):
            self._remove_info(message)
        # Handle message /start
        @self.bot.message_handler(commands=["start"])
        def about(message):
            self._about(message)
        # Khởi tạo thông tin kết nối đến Database
        self.database = 'data.db'
        self.connection_db = sqlite3.connect(self.database, check_same_thread=False)
        self.cursor = self.connection_db.cursor()
        # Chrome driver
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_argument("--headless")
        self.options.add_argument("--window-size=%s" % "1280,1024")


    # Get dữ liệu từ Instagram
    def _get_info_instagram(self, url_instagram, contributor):
        headersList = {
            "Accept": "*/*",
        }
        payload = ""
        try:
            response = requests.request("GET", url_instagram, data=payload,  headers=headersList)
            data = BeautifulSoup(response.text, "html5lib")
            info = str(data.title).split('•')[0][7:]

            idx = (str(data).index('"profile_pic_url":'))
            url_pic = (str(data)[idx+19:idx+500].split('"')[0].replace('\\', ''))
            result = self.cursor.execute('SELECT COUNT(URL) FROM main WHERE URL = ?', (str(url_instagram),))
            if (int(result.fetchone()[0]) == 0):
                self.cursor.execute('INSERT INTO main (URL, USERNAME, URL_PIC, CONTRIBUTORS) VALUES(?, ?, ?, ?)', (url_instagram, info.strip(), url_pic, contributor))
                self.connection_db.commit()
                return 1    
            else:
                return 0
        except Exception as e:
            return 2

    # Get dữ liệu từ Tiktok
    def _get_info_tiktok(self, url_tiktok, contributor):
        try:
            self.driver = webdriver.Chrome(executable_path = '/usr/lib/chromium-browser/chromedriver', chrome_options=self.options)
            self.driver.get(url_tiktok)
            profile_picture = self.driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div/div[1]/div[1]/div[1]/span/img').get_attribute("src")
            title = self.driver.title
            user_name = str(title)[:str(title).index("TikTok")]

            result = self.cursor.execute('SELECT COUNT(URL) FROM main WHERE URL = ?', (str(url_tiktok),))
            if (int(result.fetchone()[0]) == 0):
                self.cursor.execute('INSERT INTO main (URL, USERNAME, URL_PIC, CONTRIBUTORS) VALUES(?, ?, ?, ?)', (url_tiktok, title.strip(), profile_picture, contributor))
                self.connection_db.commit()
                return 1    
            else:
                return 0
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
                        result = self._get_info_instagram(url, contributor)
                        if result == 1:
                            self.bot.reply_to(message, "🌟<b>XIN CHÂN THÀNH CẢM ƠN SỰ ĐÓNG GÓP CỦA BẠN</b>🌟\nCảm ơn sự đóng góp của bạn làm cho cộng đồng ngày càng phát triển, đời sống của anh em được cải thiện.\nXin vinh danh sự đóng góp này, bravo!!!")
                        elif result == 0:
                            self.bot.reply_to(message, "Sorry bạn, hình như profile đã được vị cao nhân nào đó đóng góp trước. Cảm ơn sự đóng góp của bạn!")
                    elif('tiktok' in str(url).lower()):
                        result = self._get_info_tiktok(url, contributor)
                        if result == 1:
                            self.bot.reply_to(message, "🌟<b>XIN CHÂN THÀNH CẢM ƠN SỰ ĐÓNG GÓP CỦA BẠN</b>🌟\nCảm ơn sự đóng góp của bạn làm cho cộng đồng ngày càng phát triển, đời sống của anh em được cải thiện.\nXin vinh danh sự đóng góp này, bravo!!!")
                        elif result == 0:
                            self.bot.reply_to(message, "Sorry bạn, hình như profile đã được vị cao nhân nào đó đóng góp trước. Cảm ơn sự đóng góp của bạn!")
                    else:
                        self.bot.reply_to(message, '<i>Hiện tại hệ thống chưa hỗ trợ trang web này. Cảm ơn vì sự đóng góp của bạn!</i>')
            except Exception as e:
                self.bot.reply_to(message, 'Vui lòng điền URL hợp lệ!')

    # Xoá dữ liệu
    def _remove_info(self, message):
        if("/remove" in str(message.text).lower()):
            try:
                if(str(message.text).split(" ")[1] != ''):
                    ID = int(str(message.text).split(" ")[1])
                    self.cursor.execute('DELETE FROM main WHERE ID = ?', (ID,))
                    self.connection_db.commit()
                    self.bot.reply_to(message, 'Xoá thành công!')
                else:
                    self.bot.reply_to(message, 'Vui lòng nhập ID cần xoá!\nXem ID tại: https://hoctap.giangpt.dev/')    
            except Exception as e:
                self.bot.reply_to(message, 'Vui lòng nhập ID cần xoá!\nXem ID tại: https://hoctap.giangpt.dev/')    

    # Xếp hạng đóng góp
    def _rank_user(self, message):
        if('/rank' in str(message.text).lower()):
            try:
                rank_users = []
                result = self.cursor.execute('SELECT COUNT(CONTRIBUTORS), CONTRIBUTORS FROM main GROUP BY CONTRIBUTORS')
                for u in result.fetchall():
                    rank_users.append({"contributor": u[1], "amount": u[0]})
                return sorted(rank_users, key=lambda d: d['amount'], reverse=True) 
            except Exception as e:
                return e

    # Giới thiệu bot
    def _about(self, message):
        if('/start' in str(message.text)):
            self.bot.reply_to(message, "Xin chào <b>" + str(message.from_user.first_name) + "</b>,\n\nMình là bot hỗ trợ học tập. Bạn có thể xem tài liệu học tập tại địa chỉ https://hoctap.giangpt.dev/ hoặc có thể đóng góp thêm tài liệu từ instagram hoặc tiktok thông qua lệnh <pre>/add https://www.instagram.com/abc</pre>")

    # Lưu cookie instagram
    def _save_cookie(self, username, password):
        self.driver.get('https://www.instagram.com/')
        sleep(10)
        # Dien username
        uname = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
        uname.send_keys(username)
        # Dien password
        upass = self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
        upass.send_keys(password)
        # Nhan phim ENTER de dang nhap
        upass.send_keys(Keys.ENTER)
        # Doi load xong
        sleep(10)
        # Luu cookie
        pickle.dump(self.driver.get_cookies(), open("insta.pkl","wb"))

    # Load cookie instagram
    def _load_cookie(self, url_instagram, contributor):
        self.driver.get("https://www.instagram.com")
        # 2.Load cookie from file
        cookies = pickle.load(open("my_cookie.pkl","rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        # 3. Refresh the self.driver
        self.driver.get(url_instagram)
        try: 
            profile_pic = self.driver.find_element(By.XPATH, '//*[@id="mount_0_0_V2"]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/div/div/span/img').get_attribute('src')
            profile_name = str(self.driver.title).split('•')[0][7:].strip()
            result = self.cursor.execute('SELECT COUNT(URL) FROM main WHERE URL = ?', (str(url_instagram),))
            if (int(result.fetchone()[0]) == 0):
                self.cursor.execute('INSERT INTO main (URL, USERNAME, URL_PIC, CONTRIBUTORS) VALUES(?, ?, ?, ?)', (url_instagram, profile_name, profile_pic, contributor))
                self.connection_db.commit()
                return 1    
            else:
                return 0
        except Exception as e:
            return 2


if __name__ == '__main__':
    via_tele = Via_Telegram()
    via_tele.bot.infinity_polling()
