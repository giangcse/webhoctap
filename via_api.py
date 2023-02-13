import json
import sqlite3

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import responses
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

class Via_api:
    def __init__(self) -> None:
        # Khởi tạo api
        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )
        self.host = '0.0.0.0'
        self.port = 80
        # Khởi tạo hàm get data
        @self.app.get('/get_data')
        async def get_data():
            respone = self._get_data()
            return respone
        # Khởi tạo hàm get videos
        @self.app.get('/get_videos')
        async def get_videos():
            respone = self._get_videos()
            return respone

        # Khởi tạo hàm get videos
        @self.app.get('/get_photos')
        async def get_photos():
            respone = self._get_photos()
            return respone

        # Render trang index
        @self.app.get("/", response_class=HTMLResponse)
        async def render_index():
            return self._render_index()

        # Render trang video
        @self.app.get("/videos", response_class=HTMLResponse)
        async def render_videos():
            return self._render_videos()
        # Render trang video
        @self.app.get("/photos", response_class=HTMLResponse)
        async def render_photos():
            return self._render_photos()

        # Khởi tạo kết nối đến db
        self.database = 'data.db'
        self.connection_db = sqlite3.connect(self.database, check_same_thread=False)
        self.cursor = self.connection_db.cursor()

    def _get_data(self):
        data = self.cursor.execute('SELECT * FROM main')
        response = []
        for i in data.fetchall():
            response.append({"id": i[0], "url": i[1], "user_name": i[2], "url_pic": i[3], "contributor": i[4]})
        return (json.loads(json.dumps(response)))
    
    def _render_index(self):
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
                <title>Profiles | Tài liệu học tập</title>
            </head>
            <body>
                <nav class="navbar navbar-expand-lg sticky-top navbar-dark bg-dark">
                    <div class="container">
                        <a class="navbar-brand" href="#">TÀI LIỆU HỌC TẬP <i class="bi bi-badge-4k-fill"></i></a>
                        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
                            <span class="navbar-toggler-icon"></span>
                        </button>
                        <div class="collapse navbar-collapse" id="navbarText">
                            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                                <li class="nav-item">
                                    <a class="nav-link active" aria-current="page" href="#">Profiles</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" aria-current="page" href="/videos">Videos</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" aria-current="page" href="/photos">Hình ảnh</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" aria-current="page" href="https://t.me/giangvirtualassistantbot">Đóng góp</a>
                                </li>
                            </ul>
                            <span class="navbar-text">
                            <select class="form-select form-select-sm" aria-label=".form-select-sm example" id="filter" onchange="loadData()">
                                <option value="instagram" selected>Instagram</option>
                                <option value="tiktok">TikTok</option>
                            </select>
                            </span>
                        </div>
                    </div>
                </nav>
                <main>
                    <div class="container position-relative overflow-hidden p-3">
                        <figure class="text-end">
                            <blockquote class="blockquote">
                                <p>Gõ /update trên <a href="https://t.me/giangvirtualassistantbot">Telegram</a> nếu mất một số ảnh.</p>
                            </blockquote>
                            <figcaption class="blockquote-footer" id="soLuong">
                            </figcaption>
                        </figure>
                        <div class="row" id="main">
                            
                        </div>
                    </div>
                </main>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
            </body>
                <script>
                    loadData();
                    function loadData(){
                        let str_in = '';
                        let str_ti = '';
                        let insta = '<i class="bi bi-instagram"></i> ';
                        let tiktok = '<i class="bi bi-tiktok"></i>';
                        let filter = document.getElementById("filter").value;
                        console.log(filter)
                        $.ajax({
                            url: '/get_data',
                            data: '',
                            type: 'GET',
                            success: function(data){
                                data = eval(data)
                                data.forEach(element => {
                                    element;
                                    let link = element.url.toString();
                                    let icon = '';
                                    if(link.includes("instagram")){
                                        icon = insta;
                                        str_in += '<a class="col-sm-2" href="'+element.url+'" style="color: #ffffff;" target="_blank"><div class="card mb-2"><img src="'+element.url_pic+'" class="card-img-top"><div class="card-img-overlay">'+icon+' '+element.user_name+'<br>ID: '+element.id+'</div></div></a>';
                                    }else if(link.includes("tiktok")){
                                        str_ti += '<a class="col-sm-2" href="'+element.url+'" style="color: #ffffff;" target="_blank"><div class="card mb-2"><img src="'+element.url_pic+'" class="card-img-top"><div class="card-img-overlay">'+icon+' '+element.user_name+'<br>ID: '+element.id+'</div></div></a>';
                                    }
                                    
                                });
                                if(filter == 'instagram')
                                    document.getElementById("main").innerHTML = str_in;
                                else
                                    document.getElementById("main").innerHTML = str_ti;
                                document.getElementById("soLuong").innerText = 'Hiện tại đã có ' + data.length + ' đóng góp từ các vị anh hùng';
                            }
                        });
                    }
                </script>
            </html>
        """
        return HTMLResponse(content=html_content, status_code=200)

    def _get_videos(self):
        data = self.cursor.execute('SELECT * FROM video')
        response = []
        for i in data.fetchall():
            response.append({"id": i[0], "url": i[1], "title": i[2], "thumbnail": i[3], "contributor": i[4]})
        return (json.loads(json.dumps(response)))

    def _render_videos(self):
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
                <title>Videos TikTok | Tài liệu học tập</title>
            </head>
            <body>
                <nav class="navbar navbar-expand-lg sticky-top navbar-dark bg-dark">
                    <div class="container">
                        <a class="navbar-brand" href="#">TÀI LIỆU HỌC TẬP <i class="bi bi-badge-4k-fill"></i></a>
                        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
                            <span class="navbar-toggler-icon"></span>
                        </button>
                        <div class="collapse navbar-collapse" id="navbarText">
                            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                                <li class="nav-item">
                                    <a class="nav-link" aria-current="page" href="/">Profiles</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link active" aria-current="page" href="#">Videos</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" aria-current="page" href="/photos">Hình ảnh</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" aria-current="page" href="https://t.me/giangvirtualassistantbot">Đóng góp</a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </nav>
                <main>
                    <div class="container position-relative overflow-hidden p-3">
                        <figure class="text-end">
                            <blockquote class="blockquote">
                                <p>Gõ /update trên <a href="https://t.me/giangvirtualassistantbot">Telegram</a> nếu mất một số ảnh.</p>
                            </blockquote>
                            <figcaption class="blockquote-footer" id="soLuong">
                            </figcaption>
                        </figure>
                        <div class="row" id="main">
                            
                        </div>
                    </div>
                </main>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
            </body>
                <script>
                    loadVideos();
                    function loadVideos(){
                        let str = '';
                        $.ajax({
                            url: '/get_videos',
                            data: '',
                            type: 'GET',
                            success: function(data){
                                data = eval(data)
                                data.forEach(element => {
                                    element;
                                    str += '<a class="col-sm-2" href="'+element.url+'" style="color: #ffffff;" target="_blank"><div class="card mb-2"><img src="'+element.thumbnail+'" class="card-img-top" ><div class="card-img-overlay"><i class="bi bi-tiktok"></i> '+element.title+'<br>ID: '+element.id+'</div></div></a>';
                                });
                                document.getElementById("main").innerHTML = str;
                                document.getElementById("soLuong").innerText = 'Hiện tại đã có ' + data.length + ' đóng góp từ các vị anh hùng';
                            }
                        });
                    }
                </script>
            </html>
        """
        return HTMLResponse(content=html_content, status_code=200)

    def _get_photos(self):
        data = self.cursor.execute('SELECT * FROM photo ORDER BY ID DESC')
        response = []
        for i in data.fetchall():
            response.append({"id": i[0], "url": i[1], "url_file": i[2], "contributor": i[3]})
        return (json.loads(json.dumps(response)))

    def _render_photos(self):
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
                    a:link {
                        text-decoration: none;
                    }
                    a:hover {
                        text-decoration: none;
                    }

                    .card:hover{
                        opacity: 80%;
                    }
                    .card-img-top {
                        width: 100%;
                        height: 20vw;
                        object-fit: cover;
                    }
                </style>
                <title>Hình ảnh | Tài liệu học tập</title>
            </head>
            <body>
                <nav class="navbar navbar-expand-lg sticky-top navbar-dark bg-dark">
                    <div class="container">
                        <a class="navbar-brand" href="#">TÀI LIỆU HỌC TẬP <i class="bi bi-badge-4k-fill"></i></a>
                        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
                            <span class="navbar-toggler-icon"></span>
                        </button>
                        <div class="collapse navbar-collapse" id="navbarText">
                            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                                <li class="nav-item">
                                    <a class="nav-link" aria-current="page" href="/">Profiles</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" aria-current="page" href="/videos">Videos</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link active" aria-current="page" href="#">Hình ảnh</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" aria-current="page" href="https://t.me/giangvirtualassistantbot">Đóng góp</a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </nav>
                <main>
                    <div class="container position-relative overflow-hidden p-3">
                        <figure class="text-end">
                            <blockquote class="blockquote">
                                <!--<p>Gõ /update trên <a href="https://t.me/giangvirtualassistantbot">Telegram</a> nếu mất một số ảnh.</p>-->
                            </blockquote>
                            <figcaption class="blockquote-footer" id="soLuong">
                            </figcaption>
                        </figure>
                        <div class="row" id="main">
                            
                        </div>
                    </div>
                </main>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
            </body>
                <script>
                    loadPhotos();
                    function loadPhotos(){
                        let str = '';
                        $.ajax({
                            url: '/get_photos',
                            data: '',
                            type: 'GET',
                            success: function(data){
                                data = eval(data)
                                data.forEach(element => {
                                    element;
                                    str += '<div class="col-sm-3" style="color: #ffffff;"><div class="card mb-2"><img src="'+element.url+'" class="card-img-top" style="max-width: 400px; height: auto; object-fit: cover;"><div class="card-img-overlay"><a href="'+element.url_file+'" style="color: #ffffff;"><i class="bi bi-download"></i></a> ID: '+element.id+'</div></div></div>';
                                });
                                document.getElementById("main").innerHTML = str;
                                document.getElementById("soLuong").innerText = 'Hiện tại đã có ' + data.length + ' đóng góp từ các vị anh hùng';
                            }
                        });
                    }
                </script>
            </html>
        """
        return HTMLResponse(content=html_content, status_code=200)

via_api = Via_api()


