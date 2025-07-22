from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth import router as auth_router
from models.detect_image import router as image_router
from models.detect_video import router as video_router
from log_routes import router as log_router

app = FastAPI()

# Allowed origins for CORS
origins = ["http://localhost:5173"]

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(image_router, prefix="/detect-image", tags=["Image Detection"])
app.include_router(video_router, prefix="/detect-video", tags=["Video Detection"])
app.include_router(log_router, prefix="/logs", tags=["Logs"])

@app.get("/")
def root():
    return {"message": "✅ Deepfake Detection API is Running"}

