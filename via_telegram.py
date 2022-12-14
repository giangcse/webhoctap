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
        # Kh峄焛 t岷 th么ng tin bot
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
            content = '<b>馃帠 DANH S脕CH 膼脫NG G脫P 馃帠</b>\n\n'
            ranks = ['馃', '馃', '馃']
            i = 1
            for u in rank_users:
                if(i==1):
                    content += str(ranks[0]) + '  @' + u['contributor'] + ' v峄沬 ' + str(u['amount']) + ' 膽贸ng g贸p.\n'
                elif(i==2):
                    content += str(ranks[1]) + '  @' + u['contributor'] + ' v峄沬 ' + str(u['amount']) + ' 膽贸ng g贸p.\n'
                elif(i==3):
                    content += str(ranks[2]) + '  @' + u['contributor'] + ' v峄沬 ' + str(u['amount']) + ' 膽贸ng g贸p.\n'
                else:
                    content += ' ' + str(i) + '     @' + u['contributor'] + ' v峄沬 ' + str(u['amount']) + ' 膽贸ng g贸p.\n'
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
        # Kh峄焛 t岷 th么ng tin k岷縯 n峄慽 膽岷縩 Database
        self.database = 'data.db'
        self.connection_db = sqlite3.connect(self.database, check_same_thread=False)
        self.cursor = self.connection_db.cursor()
        # Chrome driver
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_argument("--headless")
        self.options.add_argument("--window-size=%s" % "1280,1024")


    # Get d峄? li峄噓 t峄? Instagram
    def _get_info_instagram_bs4(self, url_instagram, contributor):
        headersList = {
            "Accept": "*/*",
        }
        payload = ""
        try:
            response = requests.request("GET", url_instagram, data=payload,  headers=headersList)
            data = BeautifulSoup(response.text, "html5lib")
            info = str(data.title).split('鈥?')[0][7:]

            idx = (str(data).index('"profile_pic_url":'))
            url_pic = (str(data)[idx+19:idx+500].split('"')[0].replace('\\', ''))
            result = self.cursor.execute('SELECT COUNT(URL) FROM main WHERE URL = ?', (str(url_instagram).split('?')[0],))
            if (int(result.fetchone()[0]) == 0):
                self.cursor.execute('INSERT INTO main (URL, USERNAME, URL_PIC, CONTRIBUTORS) VALUES(?, ?, ?, ?)', (str(url_instagram).split('?')[0], info.strip(), self._upload_avatar(url_pic), contributor))
                self.connection_db.commit()
                return 1
            else:
                return 0  
        except Exception as e:
            return 2

    # Get d峄? li峄噓 t峄? Instagram
    def _get_info_instagram_selenium(self, url_instagram, contributor):
        try:
            self.driver = webdriver.Chrome(executable_path = '/usr/lib/chromium-browser/chromedriver', chrome_options=self.options)
            self.driver.get(url_instagram)
            # 膼峄 load xong
            sleep(10)
            uname = str(self.driver.title).split('@')[1]
            uname = uname.split(')')[0]
            url_pic = self.driver.find_element(By.CSS_SELECTOR, '[alt="'+str(uname)+'\'s profile picture"]').get_attribute('src')

            result = self.cursor.execute('SELECT COUNT(URL) FROM main WHERE URL = ?', (str(url_instagram),))
            if (int(result.fetchone()[0]) == 0):
                self.cursor.execute('INSERT INTO main (URL, USERNAME, URL_PIC, CONTRIBUTORS) VALUES(?, ?, ?, ?)', (url_instagram, uname.strip(), self._upload_avatar(url_pic), contributor))
                self.connection_db.commit()
                return 1    
            else:
                return 0
        except Exception as e:
            return 2

    # Get d峄? li峄噓 t峄? Tiktok
    def _get_info_tiktok(self, url_tiktok, contributor):
        try:
            self.driver = webdriver.Chrome(executable_path = '/usr/lib/chromium-browser/chromedriver', chrome_options=self.options)
            self.driver.get(url_tiktok)
            profile_picture = self.driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div/div[1]/div[1]/div[1]/span/img').get_attribute("src")
            title = self.driver.title
            user_name = str(title)[:str(title).index("TikTok")]

            result = self.cursor.execute('SELECT COUNT(URL) FROM main WHERE URL = ?', (str(url_tiktok),))
            if (int(result.fetchone()[0]) == 0):
                self.cursor.execute('INSERT INTO main (URL, USERNAME, URL_PIC, CONTRIBUTORS) VALUES(?, ?, ?, ?)', (url_tiktok, user_name.strip(), self._upload_avatar(profile_picture), contributor))
                self.connection_db.commit()
                return 1    
            else:
                return 0
        except Exception as e:
            return 0

    # Get d峄? li峄噓 t峄? Facebook
    def _get_info_facebook(self, url_facebook, contributor):
        try:
            self.driver = webdriver.Chrome(executable_path = '/usr/lib/chromium-browser/chromedriver', chrome_options=self.options)
            self.driver.get(url_facebook)
            profile_picture = self.driver.find_element(By.XPATH, '//*[@id="mount_0_0_Z2"]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[1]/div/a/div/svg/g/image').get_attribute("xlink:href")
            title = self.driver.title
            user_name = str(title)[:str(title).index("|")]

            result = self.cursor.execute('SELECT COUNT(URL) FROM main WHERE URL = ?', (str(url_facebook),))
            if (int(result.fetchone()[0]) == 0):
                self.cursor.execute('INSERT INTO main (URL, USERNAME, URL_PIC, CONTRIBUTORS) VALUES(?, ?, ?, ?)', (url_facebook, user_name.strip(), self._upload_avatar(profile_picture), contributor))
                self.connection_db.commit()
                return 1    
            else:
                return 0
        except Exception as e:
            return 0

    # Get d峄? li峄噓 video tiktok
    def _get_video_tiktok(self, url_tiktok, contributor):
        try:
            self.driver = webdriver.Chrome(executable_path = '/usr/lib/chromium-browser/chromedriver', chrome_options=self.options)
            self.driver.get(url_tiktok)

            title = self.driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[1]/div[3]/div[1]/div[1]/div[2]/div').text
            thumbnail = self.driver.find_element(By.XPATH, '/html/head/meta[27]').get_attribute("content")
            # return(title + thumbnail)
            result = self.cursor.execute('SELECT COUNT(URL) FROM video WHERE URL = ?', (str(url_tiktok),))

            if(int(result.fetchone()[0]) == 0):
                self.cursor.execute('INSERT INTO video (URL, TITLE, THUMBNAIL, CONTRIBUTORS) VALUES(?, ?, ?, ?)', (url_tiktok, title, self._upload_image(thumbnail), contributor))
                self.connection_db.commit()
                return (1)
            else:
                return 0
        except Exception as e:
            return 2

    # Th锚m m峄沬 d峄? li峄噓
    def _add_info(self, message):
        if('/add' in str(message.text).lower()):
            try:
                url = str(message.text).split(' ')[1]
                contributor = str(message.from_user.username)
                if(validators.url(url)):
                    if('instagram' in str(url).lower()):
                        result = self._get_info_instagram_bs4(url, contributor)
                        if result == 1:
                            self.bot.reply_to(message, "馃専<b>XIN CH脗N TH脌NH C岷 茽N S峄? 膼脫NG G脫P C峄 B岷燦</b>馃専\nC岷 啤n s峄? 膽贸ng g贸p c峄 b岷 l脿m cho c峄檔g 膽峄搉g ng脿y c脿ng ph谩t tri峄僴, 膽峄漣 s峄憂g c峄 anh em 膽瓢峄 c岷 thi峄噉.\nXin vinh danh s峄? 膽贸ng g贸p n脿y, bravo!!!")
                        elif result == 0:
                            self.bot.reply_to(message, "Sorry b岷, h矛nh nh瓢 profile 膽茫 膽瓢峄 v峄? cao nh芒n n脿o 膽贸 膽贸ng g贸p tr瓢峄沜. C岷 啤n s峄? 膽贸ng g贸p c峄 b岷!")
                        else:
                            self.bot.reply_to(message, "Ops! Server 膽茫 b峄? Instagram block IP do c贸 qu谩 nhi峄乽 request trong kho岷 th峄漣 gian ng岷痭. B岷 vui l貌ng th锚m l岷 sau v脿i gi峄? nh茅!")
                    elif('tiktok' in str(url).lower()):
                        result = self._get_info_tiktok(url, contributor)
                        if result == 1:
                            self.bot.reply_to(message, "馃専<b>XIN CH脗N TH脌NH C岷 茽N S峄? 膼脫NG G脫P C峄 B岷燦</b>馃専\nC岷 啤n s峄? 膽贸ng g贸p c峄 b岷 l脿m cho c峄檔g 膽峄搉g ng脿y c脿ng ph谩t tri峄僴, 膽峄漣 s峄憂g c峄 anh em 膽瓢峄 c岷 thi峄噉.\nXin vinh danh s峄? 膽贸ng g贸p n脿y, bravo!!!")
                        elif result == 0:
                            self.bot.reply_to(message, "Sorry b岷, h矛nh nh瓢 profile 膽茫 膽瓢峄 v峄? cao nh芒n n脿o 膽贸 膽贸ng g贸p tr瓢峄沜. C岷 啤n s峄? 膽贸ng g贸p c峄 b岷!")
                    elif('facebook' in str(url).lower()):
                        result = self._get_info_facebook(url, contributor)
                        if result == 1:
                            self.bot.reply_to(message, "馃専<b>XIN CH脗N TH脌NH C岷 茽N S峄? 膼脫NG G脫P C峄 B岷燦</b>馃専\nC岷 啤n s峄? 膽贸ng g贸p c峄 b岷 l脿m cho c峄檔g 膽峄搉g ng脿y c脿ng ph谩t tri峄僴, 膽峄漣 s峄憂g c峄 anh em 膽瓢峄 c岷 thi峄噉.\nXin vinh danh s峄? 膽贸ng g贸p n脿y, bravo!!!")
                        elif result == 0:
                            self.bot.reply_to(message, "Sorry b岷, h矛nh nh瓢 profile 膽茫 膽瓢峄 v峄? cao nh芒n n脿o 膽贸 膽贸ng g贸p tr瓢峄沜. C岷 啤n s峄? 膽贸ng g贸p c峄 b岷!")
                    else:
                        self.bot.reply_to(message, '<i>Hi峄噉 t岷 h峄? th峄憂g ch瓢a h峄? tr峄? trang web n脿y. C岷 啤n v矛 s峄? 膽贸ng g贸p c峄 b岷!</i>')
            except Exception as e:
                self.bot.reply_to(message, 'Vui l貌ng 膽i峄乶 URL h峄 l峄?!')

    # Th锚m d峄? li峄噓 video tiktok
    def _add_video(self, message):
        if('/clip' in str(message.text).lower()):
            try:
                url = str(message.text).split(' ')[1]
                contributor = str(message.from_user.username)
                if(validators.url(url)):
                    result = self._get_video_tiktok(url, contributor)
                    if(result == 1):
                        self.bot.reply_to(message, "馃専<b>XIN CH脗N TH脌NH C岷 茽N S峄? 膼脫NG G脫P C峄 B岷燦</b>馃専\nC岷 啤n s峄? 膽贸ng g贸p c峄 b岷 l脿m cho c峄檔g 膽峄搉g ng脿y c脿ng ph谩t tri峄僴, 膽峄漣 s峄憂g c峄 anh em 膽瓢峄 c岷 thi峄噉.\nXin vinh danh s峄? 膽贸ng g贸p n脿y, bravo!!!")
                    elif result == 0:
                        self.bot.reply_to(message, "Sorry b岷, h矛nh nh瓢 profile 膽茫 膽瓢峄 v峄? cao nh芒n n脿o 膽贸 膽贸ng g贸p tr瓢峄沜. C岷 啤n s峄? 膽贸ng g贸p c峄 b岷!")
            except Exception as e:
                self.bot.reply_to(message, 'Vui l貌ng 膽i峄乶 URL h峄 l峄?!')

    # Xo谩 d峄? li峄噓
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
                    self.bot.reply_to(message, 'Xo谩 th脿nh c么ng!')
                else:
                    self.bot.reply_to(message, 'Vui l貌ng nh岷璸 ID c岷 xo谩!\nXem ID t岷: https://hoctap.giangpt.dev/')    
            except Exception as e:
                self.bot.reply_to(message, 'Vui l貌ng nh岷璸 ID c岷 xo谩!\nXem ID t岷: https://hoctap.giangpt.dev/')    

    # X岷縫 h岷g 膽贸ng g贸p
    def _rank_user(self, message):
        if('/rank' in str(message.text).lower()):
            try:
                rank_users = []
                result_profiles = self.cursor.execute('select count(CONTRIBUTORS), CONTRIBUTORS from (select a.CONTRIBUTORS, a.URL from main a union select b.CONTRIBUTORS, b.URL from video b union select c.CONTRIBUTORS, c.URL from photo c) group by CONTRIBUTORS')
                for u in result_profiles.fetchall():
                    rank_users.append({"contributor": u[1], "amount": u[0]})
                return sorted(rank_users, key=lambda d: d['amount'], reverse=True) 
            except Exception as e:
                return e

    # Gi峄沬 thi峄噓 bot
    def _about(self, message):
        if('/start' in str(message.text)):
            self.bot.reply_to(message, "Xin ch脿o <b>" + str(message.from_user.first_name) + "</b>,\n\n<b>Th锚m profile Instagram</b>\n<pre>/add https://instagram.com/USERNAME</pre>\n<b>Th锚m profile TikTok</b>\n<pre>/add https://www.tiktok.com/@USERNAME</pre>\n<b>Th锚m video TikTok</b>\n<pre>/clip https://vt.tiktok.com/ID_VIDEO</pre>\n<b>Ho岷穋 c贸 th峄? g峄璱 岷h cho bot, l瓢u 媒 nh峄? ch峄峮 </b><em>Compress Images</em>.\n<b>Xo谩 profile</b>\n<pre>/remove profile [ID]</pre>\n<b>Xo谩 video</b>\n<pre>/remove clip [ID]</pre>\n<b>Xo谩 岷h</b>\n<pre>/remove photo [ID]</pre>\n<b>C岷璸 nh岷璽 </b><pre>/update</pre>\n<b>Danh s谩ch 膽贸ng g贸p</b>\n<pre>/rank</pre>")

    # C岷璸 nh岷璽 DB khi avatar l峄梚
    def _update(self, message):
        if('/update' in str(message.text)):
            headersList = {
                "Accept": "*/*",
            }
            payload = ""
            self.bot.reply_to(message, '膼ang th峄眂 hi峄噉 update. Vui l貌ng 膽峄 trong gi芒y l谩t!')
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
                    elif(int(response.status_code) == 403):
                        self.cursor.execute('DELETE FROM main WHERE ID = ?', (id,))
                        self.connection_db.commit()
                        self._get_info_tiktok(url, contributor)
                    sleep(15)
                self.bot.reply_to(message, '膼茫 update th脿nh c么ng!')
            except Exception as e:
                print(e)

    # H脿m upload h矛nh 岷h
    def _upload_image(self, message):
        try:
            # if('/pic' in str(message.text)):
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
                    self.cursor.execute('INSERT INTO photo (URL, URL_FILE, CONTRIBUTORS) VALUES (?, ?, ?)', (url_imgur, url_imgur, contributor))
                    self.connection_db.commit()
                    self.bot.reply_to(message, "馃専<b>XIN CH脗N TH脌NH C岷 茽N S峄? 膼脫NG G脫P C峄 B岷燦</b>馃専\nC岷 啤n s峄? 膽贸ng g贸p c峄 b岷 l脿m cho c峄檔g 膽峄搉g ng脿y c脿ng ph谩t tri峄僴, 膽峄漣 s峄憂g c峄 anh em 膽瓢峄 c岷 thi峄噉.\nXin vinh danh s峄? 膽贸ng g贸p n脿y, bravo!!!")
        except Exception:
            self.bot.reply_to(message, 'Th锚m 岷h kh么ng th脿nh c么ng, vui l貌ng ch峄峮 h矛nh 岷h v脿 ch峄峮 "Compress images".')
    
    # H脿m upload 岷h avatar
    def _upload_avatar(self, url_img):
        try:
            # if('/pic' in str(message.text)):
                url = "https://api.imgur.com/3/image"
                payload={'image': url_img}
                files=[]
                headers = {
                'Authorization': 'Client-ID 306f7cc6448a694'
                }

                response = requests.request("POST", url, headers=headers, data=payload, files=files)
                res = json.loads(response.text)

                if(int(res['status']) == 200):
                    return res['data']['link']
        except Exception:
            return False

if __name__ == '__main__':
    via_tele = Via_Telegram()
    via_tele.bot.infinity_polling()
