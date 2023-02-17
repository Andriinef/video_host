from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


class UploadVideo(BaseModel):
    title: str
    description: str


class GetListUserVideo(BaseModel):
    id: int
    title: str
    description: str


class GetVideo(BaseModel):
    user: User


class Message(BaseModel):
    message: str
