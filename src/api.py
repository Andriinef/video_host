import os
import shutil
from typing import List

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse

from .models import Video
from .schemas import GetVideo, Message, UploadVideo, User

app_router = APIRouter()


@app_router.post("/")
async def update_video(
    title: str = Form(...),
    description: str = Form(...),
    tags: List[str] = Form(...),
    file_video: UploadFile = File(),
) -> dict:
    info = UploadVideo(title=title, description=description, tags=tags)
    # create the uploads folder if it doesn't exist
    os.makedirs("uploads_video", exist_ok=True)
    file_path = os.path.join("uploads_video", str(file_video.filename))
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file_video.file, buffer)

    return {"file_name": file_video.filename, "info": info}


@app_router.post("/img")
async def update_image(files_image: List[UploadFile] = File()) -> dict:
    # create the uploads folder if it doesn't exist
    os.makedirs("uploads_image", exist_ok=True)
    for image in files_image:
        file_path = os.path.join("uploads_image", str(image.filename))
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    return {"file_name": "Good"}


@app_router.post("/info")
async def info_set(info: UploadVideo):
    return info


@app_router.get("/info_video", response_model=GetVideo, responses={404: {"model": Message}})
async def get_info_video() -> JSONResponse:
    user_up = User(**{"id": 25, "name": "Piter"})
    video_up = UploadVideo(**{"title": "Test", "description": "Description", "tags": ["qwe", "asd", "zxc"]})
    info = GetVideo(user=user_up, video=video_up)
    return JSONResponse(status_code=200, content=info.dict())


@app_router.post("/video")
async def create_video(video: Video):
    await video.save()
    return video
