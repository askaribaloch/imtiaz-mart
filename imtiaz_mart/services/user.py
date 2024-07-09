# app/services/user.py

from fastapi import HTTPException, Depends
from sqlmodel import Session, select
from passlib.context import CryptContext
from app.db.models import User
from app.schemas.user import UserCreate, UserRead
from app.core.security import verify_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_user_by_email(db: Session, email: str):
    user = db.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return user

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_current_user(db: Session, token: str = Depends(verify_token)):
    user = get_user(db, token["sub"])
    return user
