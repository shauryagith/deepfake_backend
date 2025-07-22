from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ----------------------------
# User Models
# ----------------------------

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str

# ----------------------------
# Detection Log Models
# ----------------------------

class DetectionLogCreate(BaseModel):
    filename: str
    result: str

class DetectionLog(BaseModel):
    id: int
    username: str
    filename: str
    result: str
    timestamp: datetime

    class Config:
        orm_mode = True
