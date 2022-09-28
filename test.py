import requests
import os
import base64
import json
import sqlite3
import time

from bs4 import BeautifulSoup

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

def _upload_img(url_img):
    url = "https://api.imgur.com/3/image"
    payload={'image': url_img}
    files=[]
    headers = {
    'Authorization': 'Client-ID 306f7cc6448a694'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    res = json.loads(response.text)
    print(res)
    url_imgur = res['data']['link']
    cursor.execute('INSERT INTO photo (URL, CONTRIBUTORS) VALUES (?, ?)', (url_imgur, 'giangptvlg'))
    conn.commit()

def _get_url(no):
    reqUrl = 'https://giangthur97.gumroad.com/products/search?user_id=6980412128632&from='+str(no)
    headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }
    payload = ""
    response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
    for i in (json.loads(response.text)['products']):
        _get_image(i['url'])

def _get_image(url):
    headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }
    payload = ""
    response = requests.request("GET", url, data=payload,  headers=headersList)
    data = BeautifulSoup(response.text, 'html5lib')
    for link in data.find_all('link', href=True):
        if('image' in str(link)):
            _upload_img(link['href'])
        time.sleep(15)

if __name__=='__main__':
    for i in range(1, 106, 9):
        _get_url(i)