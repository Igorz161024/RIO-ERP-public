import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from dotenv import load_dotenv

# 🔑 Завантажуємо змінні з .env.prod
load_dotenv(dotenv_path=".env.prod")

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")  # fallback якщо .env не підвантажився
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 🔒 Налаштування для паролів
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Створює JWT токен з даними користувача.
    У data можна передати {"sub": username, "role": "accountant"}.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    """
    Перевіряє токен і повертає payload.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user_role(token: str = Depends(oauth2_scheme)):
    """
    Витягує роль користувача з токена.
    """
    payload = verify_token(token)
    role = payload.get("role")
    if role is None:
        raise HTTPException(status_code=403, detail="Role not found in token")
    return role
