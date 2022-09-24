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
        @self.app.get("/", response_class=HTMLResponse)
        async def render_index():
            return self._render_index()
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
            
                <!-- Modal -->
                <div class="modal fade" id="myModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel">Đóng góp link</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="input-group flex-nowrap">
                                <span class="input-group-text" id="addon-wrapping"><i class="bi bi-instagram"></i></span>
                                <input type="text" class="form-control" placeholder="Profile URL" aria-label="Profile URL" aria-describedby="addon-wrapping" id="url-input" required>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Đóng</button>
                            <button type="button" class="btn btn-primary" onclick="addNew()">Thêm</button>
                        </div>
                    </div>
                    </div>
                </div>

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
                                    str += '<div class="col-sm-2"><div class="card mb-2"><a href="'+element.url+'" class="card-title" style="color: #ffffff;" target="_blank"><img src="'+element.url_pic+'" class="card-img-top"><div class="card-img-overlay">'+icon+' '+element.user_name+'<br>ID: '+element.id+'</div></a></div></div>';
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
if __name__=='__main__':
    via_api.run()

