from fastapi import FastAPI

from src.api import app_router

app = FastAPI()


app.include_router(app_router)
