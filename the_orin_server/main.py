
from client.aws import aws_client

import uvicorn
from pathlib import Path
from uuid import uuid7

from fastapi import FastAPI, UploadFile

FRONTEND_DIR = Path(__file__).parent / "frontend"

app = FastAPI()

@app.post("/upload-files/")
def create_upload_file(file: UploadFile):
    file.filename = f"{uuid7()}-{file.filename}"
    res = aws_client.upload_to_s3(file)
    return res
    
@app.get('/s3-files/')
def s3_files():
    return aws_client.get_s3_files()

app.frontend("/", directory=FRONTEND_DIR, fallback="index.html")

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)
