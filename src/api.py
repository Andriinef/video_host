import os
import shutil
from typing import List

from fastapi import APIRouter, BackgroundTasks, File, Form, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.templating import Jinja2Templates

from .models import User, Video
from .schemas import GetListUserVideo, GetVideo, Message, UploadVideo
from .services import save_video

app_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@app_router.post("/")
async def update_video(
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(),
):
    user = await User.objects.first()
    return await save_video(user, file, title, description, background_tasks)


@app_router.get("/video/{video_pk}", responses={404: {"model": Message}})
async def get_video(video_pk: int):
    file = await Video.objects.select_related("user").get(pk=video_pk)
    file_like = open(file.file, mode="rb")
    return StreamingResponse(file_like, media_type="video/mp4")


@app_router.post("/img")
async def update_image(files_image: List[UploadFile] = File()) -> dict:
    # create the uploads folder if it doesn't exist
    os.makedirs("media/uploads_image", exist_ok=True)
    for image in files_image:
        file_path = os.path.join("media/uploads_image", str(image.filename))
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    return {"file_name": "Good"}


@app_router.get("/user/{user_pk}", response_model=List[GetListUserVideo])
async def get_list_user_video(user_pk: int):
    video_list = await Video.objects.filter(user=user_pk).all()
    return video_list


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


@app_router.post("/user")
async def create_user(user: User):
    await user.save()
    return user
