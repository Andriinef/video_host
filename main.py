import os
import shutil
from typing import List

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/")
async def update_video(file_video: UploadFile = File()) -> dict:
    # create the uploads folder if it doesn't exist
    os.makedirs("uploads_video", exist_ok=True)
    file_path = os.path.join("uploads_video", str(file_video.filename))
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file_video.file, buffer)

    return {"file_name": file_video.filename}


@app.post("/img")
async def update_image(files_image: List[UploadFile] = File()) -> dict:
    # create the uploads folder if it doesn't exist
    os.makedirs("uploads_image", exist_ok=True)
    for image in files_image:
        file_path = os.path.join("uploads_image", str(image.filename))
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    return {"file_name": "Good"}
