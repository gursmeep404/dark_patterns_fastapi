from fastapi import APIRouter, UploadFile, File
from app.process_video import analyze_video_pipeline

router = APIRouter()

@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    return await analyze_video_pipeline(file)
