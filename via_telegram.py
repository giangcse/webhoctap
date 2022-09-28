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
        # Handle message /clip
        @self.bot.message_handler(commands=['clip'])
        def add_clip(message):
            self._add_video(message)
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
        # Handle message /update
        @self.bot.message_handler(commands=['update'])
        def update(message):
            self._update(message)
        # Handle photo
        @self.bot.message_handler(content_types=['photo', 'document'])
        def handle_photo(message):
            self._upload_image(message)
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
    def _get_info_instagram_bs4(self, url_instagram, contributor):
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

    # Get dữ liệu từ Instagram
    def _get_info_instagram_selenium(self, url_instagram, contributor):
        try:
            self.driver = webdriver.Chrome(executable_path = '/usr/lib/chromium-browser/chromedriver', chrome_options=self.options)
            self.driver.get(url_instagram)
            # Đợi load xong
            sleep(10)
            uname = str(self.driver.title).split('@')[1]
            uname = uname.split(')')[0]
            url_pic = self.driver.find_element(By.CSS_SELECTOR, '[alt="'+str(uname)+'\'s profile picture"]').get_attribute('src')

            result = self.cursor.execute('SELECT COUNT(URL) FROM main WHERE URL = ?', (str(url_instagram),))
            if (int(result.fetchone()[0]) == 0):
                self.cursor.execute('INSERT INTO main (URL, USERNAME, URL_PIC, CONTRIBUTORS) VALUES(?, ?, ?, ?)', (url_instagram, uname.strip(), url_pic, contributor))
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
                self.cursor.execute('INSERT INTO main (URL, USERNAME, URL_PIC, CONTRIBUTORS) VALUES(?, ?, ?, ?)', (url_tiktok, user_name.strip(), profile_picture, contributor))
                self.connection_db.commit()
                return 1    
            else:
                return 0
        except Exception as e:
            return 0

    # Get dữ liệu video tiktok
    def _get_video_tiktok(self, url_tiktok, contributor):
        try:
            self.driver = webdriver.Chrome(executable_path = '/usr/lib/chromium-browser/chromedriver', chrome_options=self.options)
            self.driver.get(url_tiktok)

            title = self.driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[1]/div[3]/div[1]/div[1]/div[2]/div').text
            thumbnail = self.driver.find_element(By.XPATH, '/html/head/meta[27]').get_attribute("content")
            # return(title + thumbnail)
            result = self.cursor.execute('SELECT COUNT(URL) FROM video WHERE URL = ?', (str(url_tiktok),))

            if(int(result.fetchone()[0]) == 0):
                self.cursor.execute('INSERT INTO video (URL, TITLE, THUMBNAIL, CONTRIBUTORS) VALUES(?, ?, ?, ?)', (url_tiktok, title, thumbnail, contributor))
                self.connection_db.commit()
                return (1)
            else:
                return 0
        except Exception as e:
            return 2

    # Thêm mới dữ liệu
    def _add_info(self, message):
        if('/add' in str(message.text).lower()):
            try:
                url = str(message.text).split(' ')[1]
                contributor = str(message.from_user.username)
                if(validators.url(url)):
                    if('instagram' in str(url).lower()):
                        result = self._get_info_instagram_bs4(url, contributor)
                        if result == 1:
                            self.bot.reply_to(message, "🌟<b>XIN CHÂN THÀNH CẢM ƠN SỰ ĐÓNG GÓP CỦA BẠN</b>🌟\nCảm ơn sự đóng góp của bạn làm cho cộng đồng ngày càng phát triển, đời sống của anh em được cải thiện.\nXin vinh danh sự đóng góp này, bravo!!!")
                        elif result == 0:
                            self.bot.reply_to(message, "Sorry bạn, hình như profile đã được vị cao nhân nào đó đóng góp trước. Cảm ơn sự đóng góp của bạn!")
                        else:
                            self.bot.reply_to(message, "Ops! Server đã bị Instagram block IP do có quá nhiều request trong khoản thời gian ngắn. Bạn vui lòng thêm lại sau vài giờ nhé!")
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

    # Thêm dữ liệu video tiktok
    def _add_video(self, message):
        if('/clip' in str(message.text).lower()):
            try:
                url = str(message.text).split(' ')[1]
                contributor = str(message.from_user.username)
                if(validators.url(url)):
                    result = self._get_video_tiktok(url, contributor)
                    if(result == 1):
                        self.bot.reply_to(message, "🌟<b>XIN CHÂN THÀNH CẢM ƠN SỰ ĐÓNG GÓP CỦA BẠN</b>🌟\nCảm ơn sự đóng góp của bạn làm cho cộng đồng ngày càng phát triển, đời sống của anh em được cải thiện.\nXin vinh danh sự đóng góp này, bravo!!!")
                    elif result == 0:
                        self.bot.reply_to(message, "Sorry bạn, hình như profile đã được vị cao nhân nào đó đóng góp trước. Cảm ơn sự đóng góp của bạn!")
            except Exception as e:
                self.bot.reply_to(message, 'Vui lòng điền URL hợp lệ!')

    # Xoá dữ liệu
    def _remove_info(self, message):
        if("/remove" in str(message.text).lower()):
            try:
                if(str(message.text).split(" ")[1] != ''):
                    if(str(message.text).split(" ")[1] == 'profile'):
                        ID = int(str(message.text).split(" ")[2])
                        self.cursor.execute('DELETE FROM main WHERE ID = ?', (ID,))
                    elif(str(message.text).split(" ")[1] == 'clip'):
                        ID = int(str(message.text).split(" ")[2])
                        self.cursor.execute('DELETE FROM video WHERE ID = ?', (ID,))
                    elif(str(message.text).split(" ")[1] == 'photo'):
                        ID = int(str(message.text).split(" ")[2])
                        self.cursor.execute('DELETE FROM photo WHERE ID = ?', (ID,))
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
                result_profiles = self.cursor.execute('select count(CONTRIBUTORS), CONTRIBUTORS from (select * from main union select * from video) group by CONTRIBUTORS')
                for u in result_profiles.fetchall():
                    rank_users.append({"contributor": u[1], "amount": u[0]})
                return sorted(rank_users, key=lambda d: d['amount'], reverse=True) 
            except Exception as e:
                return e

    # Giới thiệu bot
    def _about(self, message):
        if('/start' in str(message.text)):
            self.bot.reply_to(message, "Xin chào <b>" + str(message.from_user.first_name) + "</b>,\n\n<b>Thêm profile Instagram</b>\n<pre>/add https://instagram.com/USERNAME</pre>\n<b>Thêm profile TikTok</b>\n<pre>/add https://www.tiktok.com/@USERNAME</pre>\n<b>Thêm video TikTok</b>\n<pre>/clip https://vt.tiktok.com/ID_VIDEO</pre>\n<b>Hoặc có thể gửi ảnh cho bot, lưu ý nhớ chọn </b><em>Compress Images</em>.\n<b>Xoá profile</b>\n<pre>/remove profile [ID]</pre>\n<b>Xoá video</b>\n<pre>/remove clip [ID]</pre>\n<b>Xoá ảnh</b>\n<pre>/remove photo [ID]</pre>\n<b>Cập nhật </b><pre>/update</pre>\n<b>Danh sách đóng góp</b>\n<pre>/rank</pre>")

    # Cập nhật DB khi avatar lỗi
    def _update(self, message):
        if('/update' in str(message.text)):
            headersList = {
                "Accept": "*/*",
            }
            payload = ""
            self.bot.reply_to(message, 'Đang thực hiện update. Vui lòng đợi trong giây lát!')
            try:
                data = self.cursor.execute('SELECT * FROM main')
                for i in data.fetchall():
                    response = requests.request("GET", i[3], data=payload,  headers=headersList)
                    id = int(i[0])
                    url = str(i[1])
                    contributor = str(i[4])
                    if(response.text == 'URL signature expired'):
                        self.cursor.execute('DELETE FROM main WHERE ID = ?', (id,))
                        self.connection_db.commit()
                        self._get_info_instagram_bs4(url, contributor)
                    elif(BeautifulSoup(response.text, 'html5lib').title == 'Access Denied'):
                        self.cursor.execute('DELETE FROM main WHERE ID = ?', (id,))
                        self.connection_db.commit()
                        self._get_info_tiktok(url, contributor)
                    sleep(15)
                self.bot.reply_to(message, 'Đã update thành công!')
            except Exception as e:
                print(e)

    # Hàm upload hình ảnh
    def _upload_image(self, message):
        try:
            file = self.bot.get_file(message.photo[-1].file_id)
            url_img = 'https://api.telegram.org/file/bot'+self.bot_token+'/'+file.file_path
            url = "https://api.imgur.com/3/image"
            payload={'image': url_img}
            files=[]
            headers = {
            'Authorization': 'Client-ID 306f7cc6448a694'
            }

            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            res = json.loads(response.text)

            if(int(res['status']) == 200):
                contributor = str(message.from_user.username)
                url_imgur = res['data']['link']
                self.cursor.execute('INSERT INTO photo (URL, CONTRIBUTORS) VALUES (?, ?)', (url_imgur, contributor))
                self.connection_db.commit()
                self.bot.reply_to(message, "🌟<b>XIN CHÂN THÀNH CẢM ƠN SỰ ĐÓNG GÓP CỦA BẠN</b>🌟\nCảm ơn sự đóng góp của bạn làm cho cộng đồng ngày càng phát triển, đời sống của anh em được cải thiện.\nXin vinh danh sự đóng góp này, bravo!!!")
        except Exception:
            self.bot.reply_to(message, 'Thêm ảnh không thành công, vui lòng chọn hình ảnh và chọn "Compress images".')

if __name__ == '__main__':
    via_tele = Via_Telegram()
    via_tele.bot.infinity_polling()
