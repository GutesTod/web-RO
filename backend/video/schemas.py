from pydantic import BaseModel

class VideoBase(BaseModel):
    ...

class UploadResponseVideo(VideoBase):
    filename: str

class DowloadVideo(VideoBase):
    filename: str