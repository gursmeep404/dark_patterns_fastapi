from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Dark Pattern Detector API")
app.include_router(router)
