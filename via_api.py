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
        self.port = 88
        # Khởi tạo hàm get data
        @self.app.get('/get_data')
        async def get_data():
            respone = self._get_data()
            return respone
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


via_api = Via_api()
if __name__=='__main__':
    via_api.run()

