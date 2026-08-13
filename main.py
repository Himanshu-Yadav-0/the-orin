from utils.utils import is_wifi_connected
from client.aws import aws_service

import uvicorn

from fastapi import FastAPI, UploadFile
from typing import Annotated

app = FastAPI()

@app.post("/upload-files/")
def create_upload_file(file: UploadFile):
    res = aws_service.upload_to_s3(file)
    return res
    
@app.get('/s3-files/')
def s3_files():
    return aws_service.get_s3_files()

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)
