from fastapi import FastAPI
from backend.video.router import video_router

app = FastAPI()

app.include_router(video_router)