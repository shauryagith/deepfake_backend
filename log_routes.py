# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from utils import get_current_user
# from database import get_db, DetectionLogModel, UserModel
# from schemas import DetectionLog

# router = APIRouter()

# @router.get("/", response_model=list[DetectionLog])
# def get_logs(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
#     logs = db.query(DetectionLogModel).filter(DetectionLogModel.user_id == current_user.id).all()
#     print(f"Retrieved logs for user {current_user.username}: {logs}")
#     return logs


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils import get_current_user
from database import get_db, DetectionLogModel, UserModel
from schemas import DetectionLog

router = APIRouter()

@router.get("/", response_model=list[DetectionLog])
def get_logs(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    logs = (
        db.query(DetectionLogModel)
        .filter(DetectionLogModel.user_id == current_user.id)
        .all()
    )

    # Map to response with username field manually
    return [
        DetectionLog(
            id=log.id,
            filename=log.filename,
            result=log.result,
            timestamp=log.timestamp,
            username=current_user.username  # manually add username
        )
        for log in logs
    ]
