import requests
import json
import pandas as pd
import uvicorn
# import pymongo
import sqlite3
import validators

from bs4 import BeautifulSoup
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi import responses
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# myclient = pymongo.MongoClient('mongodb://localhost:27017')
# mydb = myclient['tailieuhoctap']
# mycol = mydb['instagram']
conn = sqlite3.connect('tailieuhoctap.db')
cursor = conn.cursor()

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
}
payload = ""

class Data(BaseModel):
    url:str

def getInfoUser_instagram(url_profile):
    try:
        response = requests.request("GET", url_profile, data=payload,  headers=headersList)

        data = BeautifulSoup(response.text, "html")
        info = str(data.title).split('•')[0][7:]

        idx = (str(data).index('"profile_pic_url":'))
        url_pic = (str(data)[idx+19:idx+500].split('"')[0].replace('\\', ''))

        # mycol.insert_one({"user_name": str(info), "profile_picture": str(url_pic), "url_profile": url_profile})
        cursor.execute('''INSERT INTO data VALUES('''+str(info)+''', '''+str(url_pic)''', '''+url_profile+''')''')
        conn.commit()
    except Exception as e:
        return e

def readFile(file_path):
    data = pd.read_csv(file_path)
    return data.iloc[:,0]

@app.get('/')
async def root():
    data = []
    for d in cursor.execute('''SELECT * FROM data'''):
        data.append({"user_name": str(d[0]), "profile_picture": str(d[1]), "url_profile": d[2]})

    return (json.loads(json.dumps(data)))

@app.get('/add')
async def add(url: str = Form(...)):
    return {"url": url}

def saveToDB():
    try:
        urls = readFile('E:\\Cong chien\\Linh tinh\\insta\\url.csv')
        data = []
        for url in urls:
            data.append(getInfoUser_instagram(url))
        return data
    except Exception as e:
        return e

if __name__=='__main__':
    # saveToDB()
    uvicorn.run("main:app", host="0.0.0.0", port=81, debug=True)
