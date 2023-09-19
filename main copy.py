from fastapi import FastAPI, UploadFile, File
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
import os

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

@app.get("/hello")
def hello():
    return {"message": "안녕하세요 파이보"}

@app.post("/upload/")
async def upload_video(video: UploadFile = File(...)):
    video_bytes = await video.read()
    with open(f"videos/{video.filename}", 'wb') as f:
        f.write(video_bytes)
    return {"filename": video.filename}

@app.get("/video/{video_name}")
async def get_video(video_name: str):
    video_path = f"videos/{video_name}"
    if os.path.exists(video_path):
        return FileResponse(video_path)
    else:
        return {"error": "Video not found"}

app.mount("/assets", StaticFiles(directory="./assets"))
app.mount("/utils", StaticFiles(directory="./utils"))
app.mount("/components", StaticFiles(directory="./components"))

@app.get("/")
def index():
    return FileResponse("index.html")