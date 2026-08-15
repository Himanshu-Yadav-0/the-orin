
from client.aws import aws_client

import uvicorn
from pathlib import Path
from uuid import uuid7

from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles

FRONTEND_DIR = Path(__file__).parent / "frontend"
ASSETS_DIR = Path(__file__).parent / "assets"

app = FastAPI()

app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

@app.post("/upload-files/")
def create_upload_file(files: list[UploadFile]):
    res = []
    for file in files: 
        file.filename = f"{uuid7()}-{file.filename}"
        res.append(aws_client.upload_to_s3(file))
    return res
    
@app.get('/s3-files/')
def s3_files():
    return aws_client.get_s3_files()

app.frontend("/", directory=FRONTEND_DIR, fallback="index.html")

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)
