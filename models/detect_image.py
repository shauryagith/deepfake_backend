import shutil
import os
from fastapi import APIRouter, File, UploadFile, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from utils import get_current_user
from database import get_db, DetectionLogModel, UserModel
from ml_model import predict_image  # ✅ Updated to return label + confidence

router = APIRouter()

@router.post("/upload")
async def detect_image(
    file: UploadFile = File(...),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # ✅ Ensure upload directory exists
    os.makedirs("temp_uploads", exist_ok=True)

    # ✅ Save uploaded image temporarily
    file_location = f"temp_uploads/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ✅ Predict using model
    prediction = predict_image(file_location)
    label = prediction["label"]
    confidence = prediction["confidence"]

    # ✅ Log result in database
    log = DetectionLogModel(
        filename=file.filename,
        result=f"{label} ({confidence}%)",
        user_id=current_user.id,
        timestamp=datetime.utcnow()
    )
    db.add(log)
    db.commit()

    # ✅ Return clean response
    return {
        "filename": file.filename,
        "label": label,
        "confidence": confidence,
        "user": current_user.username,
        "timestamp": log.timestamp.isoformat()
    }

