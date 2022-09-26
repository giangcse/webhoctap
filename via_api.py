import json
import uvicorn
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
        # Render trang index
        @self.app.get("/", response_class=HTMLResponse)
        async def render_index():
            return self._render_index()

        # Render trang video
        @self.app.get("/videos", response_class=HTMLResponse)
        async def render_videos():
            return self._render_videos()
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

    def _get_videos(self):
        data = self.cursor.execute('SELECT * FROM video')
        response = []
        for i in data.fetchall():
            response.append({"id": i[0], "url": i[1], "title": i[2], "thumbnail": i[3], "contributor": i[4]})
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
                <title>Profiles | Tài liệu học tập</title>
            </head>
            <body>
                <header class="site-header sticky-top py-1 navbar-custom">
                    <nav class="container d-flex flex-column flex-md-row justify-content-between">
                    <b class="py-2" style="color: #ffffff;"><i class="bi bi-journal-bookmark-fill"></i> TÀI LIỆU HỌC TẬP</b>
                    <a href="/videos" class="py-2 d-none d-md-inline-block" style="color: #ffffff;">Videos</a>
                    </nav>
                </header>
                <main>
                    <div class="container position-relative overflow-hidden p-3">
                        <figure class="text-end">
                            <blockquote class="blockquote">
                                <p>Các vị anh hùng hãy cẩn trọng. Những trang sử này dễ gây mất hạnh phúc gia đình.</p>
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
                        let str = '';
                        let insta = '<i class="bi bi-instagram"></i> ';
                        let tiktok = '<i class="bi bi-tiktok"></i>';
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
                                    }else if(link.includes("tiktok")){
                                        icon = tiktok;
                                    }
                                    str += '<a class="col-sm-2" href="'+element.url+'" style="color: #ffffff;" target="_blank"><div class="card mb-2"><img src="'+element.url_pic+'" class="card-img-top"><div class="card-img-overlay">'+icon+' '+element.user_name+'<br>ID: '+element.id+'</div></div></a>';
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
                <title>Videos TikTok | Tài liệu học tập</title>
            </head>
            <body>
                <header class="site-header sticky-top py-1 navbar-custom">
                    <nav class="container d-flex flex-column flex-md-row justify-content-between">
                    <b class="py-2" style="color: #ffffff;"><i class="bi bi-journal-bookmark-fill"></i> TÀI LIỆU HỌC TẬP</b>
                    <a href="/" class="py-2 d-none d-md-inline-block" style="color: #ffffff;">Profiles</a>
                    </nav>
                </header>
                <main>
                    <div class="container position-relative overflow-hidden p-3">
                        <figure class="text-end">
                            <blockquote class="blockquote">
                                <p>Các vị anh hùng hãy cẩn trọng. Những trang sử này dễ gây mất hạnh phúc gia đình.</p>
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
                    function direct(url) {
                        window.location.replace(url);
                        alert(url);
                    }
                </script>
            </html>
        """
        return HTMLResponse(content=html_content, status_code=200)


via_api = Via_api()
if __name__=='__main__':
    via_api.run()

