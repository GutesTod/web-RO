from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse

import os

from .schemas import UploadResponseVideo, DowloadVideo

video_router = APIRouter(prefix="/video", tags=['Видео'])

UPLOAD_DIR = "uploads"

@video_router.post('/upload/', response_model=UploadResponseVideo)
async def upload_video(file: UploadFile = File(...)):

    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Файл является не видео-файлом!")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return JSONResponse(
        content={
            "filename" : file.filename
        },
        status_code=200
    )

def delete_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Файл {file_path} был удален.")

@video_router.post('/download/', response_class=FileResponse)
async def download_video(request: DowloadVideo, background_tasks: BackgroundTasks):
    file_path = os.path.join(UPLOAD_DIR, request.filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден!")
    
    response = FileResponse(file_path, media_type="application/octet-stream", filename=request.filename)

    background_tasks.add_task(delete_file, file_path)

    return response
    
