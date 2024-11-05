from fastapi import APIRouter, File, UploadFile, HTTPException, Response
from fastapi.responses import FileResponse

import os

from .schemas import UploadResponseVideo, DowloadVideo

video_router = APIRouter(prefix="/video", tags=['Видео'])

UPLOAD_DIR = "uploads"

@video_router.post('/upload/', response_model=UploadResponseVideo)
async def upload_video(file: UploadFile = File(...)):
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Файл является не видео-файлом!")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return Response(
        content={
            "filename" : file.filename
        },
        status_code=200
    )

@video_router.post('/download/', response_class=FileResponse)
async def download_video(request: DowloadVideo):
    file_path = os.path.join(UPLOAD_DIR, request.filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден!")
    
    response = FileResponse(file_path, media_type="application/octet-stream", filename=request.filename)

    @response.on_send_complete
    async def delete_file():
        os.remove(file_path)
        print(f"{request.filename} удален!")

    return response
    
