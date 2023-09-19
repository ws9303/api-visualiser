from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from blur import blur_video
import os

UPLOAD_DIR = Path() / 'uploads'

app = FastAPI()

origins = [
    "http://127.0.0.1:8000"
    "http://127.0.0.1:5173",    # 또는 "http://localhost:5173"
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/uploadfile/")
async def upload_video(video_input: UploadFile = File(...)):
    data = await video_input.read()
    save_to = UPLOAD_DIR / video_input.filename
    blur_to = UPLOAD_DIR / 'blur' / video_input.filename
    with open(save_to, 'wb') as f:
        f.write(data)
    blur_video(f'./{save_to}')
    return FileResponse(blur_to, media_type='application/octet-stream',filename=f'blur_{video_input.filename}')
    # return {"fileloc" : f'./{save_to}'}


@app.get("/video/{video_name}")
async def get_video(video_name: str):
    video_path = f"uploads/{video_name}"
    if os.path.exists(video_path):
        # return FileResponse(video_path)
        return video_path
        # return FileResponse(video_path, media_type='application/octet-stream',filename=f'blur_{video_name}')
    else:
        return {"error": "Video not found"}

app.mount("/assets", StaticFiles(directory="./assets"))
app.mount("/utils", StaticFiles(directory="./utils"))
app.mount("/components", StaticFiles(directory="./components"))

@app.get("/")
def index():
    return FileResponse("index.html")