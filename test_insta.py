import requests

from bs4 import BeautifulSoup

reqUrl = "https://instagram.com/giangpt.vlg"

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
}

payload = ""

response = requests.request("GET", reqUrl, data=payload,  headers=headersList)

print(response.text)