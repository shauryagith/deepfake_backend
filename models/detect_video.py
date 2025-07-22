from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
from utils import get_current_user
from database import get_db, DetectionLogModel, UserModel
from ml_model import predict_video  # ✅ Import video prediction
import shutil
from datetime import datetime
import os

router = APIRouter()

@router.post("/upload")
async def detect_video(
    file: UploadFile = File(...),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ✅ Ensure temp folder exists
    os.makedirs("temp_uploads", exist_ok=True)

    # ✅ Save video file
    file_location = f"temp_uploads/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ✅ Predict with ML model
    prediction = predict_video(file_location)
    label = prediction["label"]
    confidence = prediction["confidence"]

    # ✅ Store result in DB
    log = DetectionLogModel(
        filename=file.filename,
        result=f"{label} ({confidence}%)",
        user_id=current_user.id,
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()

    return {
        "filename": file.filename,
        "label": label,
        "confidence": confidence,
        "user": current_user.username,
        "timestamp": log.timestamp
    }
