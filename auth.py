from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from utils import create_access_token, get_current_user
from schemas import User, UserCreate, Token
from sqlalchemy.orm import Session
from database import get_db, Base, engine, UserModel

router = APIRouter()

# ✅ Ensure DB tables are created
Base.metadata.create_all(bind=engine)

# ✅ Signup endpoint
@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
   
    existing_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    # print(f"Checking for existing user: {existing_user}")
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = bcrypt.hash(user.password)
    new_user = UserModel(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token}

# ✅ Login endpoint
@router.post("/login", response_model=Token)
def login(form_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    
    if not user or not bcrypt.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ Get current user profile
@router.get("/me", response_model=User)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user
