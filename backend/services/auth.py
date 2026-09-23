import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from backend.models.user import User

# Завантаження секретів
load_dotenv(dotenv_path=".env.prod")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------------------
# Паролі
# -------------------------------
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# -------------------------------
# Аутентифікація
# -------------------------------
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

# -------------------------------
# Токени
# -------------------------------
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user: User, db: Session) -> str:
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"sub": user.username, "role": user.role, "exp": expire}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    user.refresh_token = token
    db.add(user); db.commit(); db.refresh(user)
    return token

def refresh_access_token(db: Session, refresh_token: str) -> str:
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        user = db.query(User).filter(User.username == username).first()
        if not user or user.refresh_token != refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token revoked")
        return create_access_token({"sub": user.username, "role": user.role})
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

def revoke_refresh_token(user: User, db: Session):
    user.refresh_token = None
    db.add(user); db.commit(); db.refresh(user)

