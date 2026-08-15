
from client.aws import aws_client

import uvicorn
from uuid import uuid7

from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.post("/upload-files/")
def create_upload_file(file: UploadFile):
    file.filename = f"{uuid7()}-{file.filename}"
    res = aws_client.upload_to_s3(file)
    return res
    
@app.get('/s3-files/')
def s3_files():
    return aws_client.get_s3_files()

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)
