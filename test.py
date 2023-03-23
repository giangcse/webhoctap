import pandas as pd
import sqlite3
import requests
import time

from bs4 import BeautifulSoup

conn = sqlite3.Connection('data.db')
cursor = conn.cursor()

def _get_info_instagram_bs4( url_instagram):
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
        result = cursor.execute('SELECT COUNT(URL) FROM main WHERE URL = ?', (str(url_instagram).split('?')[0],))
        if (int(result.fetchone()[0]) == 0):
            cursor.execute('INSERT INTO main (URL, USERNAME, URL_PIC, CONTRIBUTORS) VALUES(?, ?, ?, ?)', (str(url_instagram).split('?')[0], info.strip(), url_pic, 'website'))
            conn.commit()
        # return JSONResponse(status_code=200, content={"result": "success"})
    except Exception as e:
        # return JSONResponse(status_code=500, content={"error": e})
        print(e)

df = pd.DataFrame(pd.read_csv('output.csv', encoding='utf8'))

for i in range(len(df)):
    _get_info_instagram_bs4(df.iloc[i]['1'])
    time.sleep(1)