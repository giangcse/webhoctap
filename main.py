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
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


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
        cursor.execute('INSERT INTO data VALUES("'+str(info)+'", "'+str(url_pic)+'", "'+str(url_profile)+'")')
        conn.commit()
    except Exception as e:
        return e

def readFile(file_path):
    data = pd.read_csv(file_path)
    return data.iloc[:,0]

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
        <!doctype html>
        <html lang="en">
        <head>
            <!-- Required meta tags -->
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            
            <!-- Bootstrap CSS -->
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.1/font/bootstrap-icons.css">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.1/jquery.js" integrity="sha512-CX7sDOp7UTAq+i1FYIlf9Uo27x4os+kGeoT7rgwvY+4dmjqV0IuE/Bl5hVsjnQPQiTOhAX1O2r2j5bjsFBvv/A==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
            <style>
                /* Modify the background color */
                
                .navbar-custom {
                    background-color: #758283;
                }
                /* Modify brand and text color */
                
                .navbar-custom .navbar-brand,
                .navbar-custom .navbar-text {
                    color: white;
                }
                a:link {
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: none;
                }

                .card:hover{
                    opacity: 80%;
                }
            </style>
            <title>Tài liệu học tập</title>
        </head>
        <body>
            <header class="site-header sticky-top py-1 navbar-custom">
                <nav class="container d-flex flex-column flex-md-row justify-content-between">
                <b class="py-2" style="color: #ffffff;">TÀI LIỆU HỌC TẬP</b>
                <b class="py-2 d-none d-md-inline-block" data-bs-toggle="modal" data-bs-target="#myModal" style="color: #ffffff;">Đóng góp</b>
                </nav>
            </header>
            <main>
                <div class="container position-relative overflow-hidden p-3">
                    <div class="row" id="main">
                        
                    </div>
                </div>
            </main>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
        </body>
        
            <!-- Modal -->
            <div class="modal fade" id="myModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                <div class="modal-content">
                    <form>
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel">Đóng góp link</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="input-group flex-nowrap">
                                <span class="input-group-text" id="addon-wrapping"><i class="bi bi-instagram"></i></span>
                                <input type="text" class="form-control" placeholder="Username" aria-label="Username" aria-describedby="addon-wrapping" id="url-input">
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Đóng</button>
                            <button type="button" class="btn btn-primary" onclick="addNew()">Thêm</button>
                        </div>
                    </form>
                </div>
                </div>
            </div>

            <script>
                loadData();
                function addNew(){
                    let d = document.getElementById("url-input").value;
                    const form = new FormData();
                form.append("url", "abc.com");

                const settings = {
                "async": true,
                "crossDomain": true,
                "url": "https://www.giangpt.dev/add",
                "method": "GET",
                "headers": {
                    "Accept": "*/*",
                    "User-Agent": "Thunder Client (https://www.thunderclient.com)"
                },
                "processData": false,
                "contentType": false,
                "mimeType": "multipart/form-data",
                "data": form
                };

                $.ajax(settings).done(function (response) {
                console.log(response);
                });
                }

                function loadData(){
                    let str = ''
                    $.ajax({
                        url: 'https://www.giangpt.dev/fillData',
                        data: '',
                        type: 'GET',
                        success: function(data){
                            // console.log(data)
                            data = eval(data)
                            data.forEach(element => {
                                // console.log(element);
                                str += '<div class="col-sm-3"><div class="card mb-3"><img src="'+element.profile_picture+'" class="card-img-top"><div class="card-img-overlay"><a href="'+element.url_profile+'" class="card-title" style="color: #ffffff;" target="_blank"><i class="bi bi-instagram"></i> '+element.user_name+'</a></div></div></div>';
                            });
                            document.getElementById("main").innerHTML = str;
                        }
                    });
                }
            </script>
        </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get('/fillData')
async def fill_data():
    data = []
    for d in cursor.execute('''SELECT * FROM data''').fetchall():
        data.append({"user_name": str(d[0]), "profile_picture": str(d[1]), "url_profile": d[2]})
    return (json.loads(json.dumps(data)))

@app.get('/add')
async def add(url: str = Form(...)):
    return {"url": url}

def saveToDB():
    try:
        urls = readFile('url.csv')
        data = []
        for url in urls:
            data.append(getInfoUser_instagram(url))
        return data
    except Exception as e:
        return e

if __name__=='__main__':
    # saveToDB()
    uvicorn.run("main:app", host="0.0.0.0", port=80)
