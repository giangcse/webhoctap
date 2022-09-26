from turtle import title
import requests
from bs4 import BeautifulSoup

reqUrl = "https://www.tiktok.com/@chiiliiu/video/7134277742723386650"

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
}

payload = ""

def get_video(url):
    try:
        response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
        data = BeautifulSoup(response.text, 'html5lib')
        title = data.title
        thumbnails = data.find("meta", attrs={'property': 'og:image'}).attrs['content']
        print(title, thumbnails)
    except Exception as e:
        print(e)

get_video(reqUrl)