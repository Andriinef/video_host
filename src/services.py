import shutil

from fastapi import BackgroundTasks, HTTPException, UploadFile

from .models import Video
from .schemas import UploadVideo


async def save_video(user, file: UploadFile, title: str, description: str, background_tasks: BackgroundTasks):
    file_name = f"media/uploads_video/{user.user_id}_{file.filename}"
    if file.content_type == "video/mp4":
        background_tasks.add_task(write_video, file_name, file)
    else:
        raise HTTPException(status_code=418)
    info = UploadVideo(title=title, description=description)
    return await Video.objects.create(file=file_name, user=user, **info.dict())


def write_video(file_name: str, file: UploadFile):
    with open(file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
