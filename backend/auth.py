import os
from dotenv import load_dotenv
from datetime import timedelta, datetime
from passlib.context import CryptContext
from jose import JWTError, jwt

# Завантаження секретів
load_dotenv(dotenv_path=".env.prod")

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")
ALGORITHM = "HS256"

# час життя токена у хвилинах (1 рік)
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Конфігурація для bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_token_expiry() -> timedelta:
    """Повертає стандартний час життя токена."""
    return timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Перевіряє пароль користувача проти bcrypt-хешу."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Генерує bcrypt-хеш для нового пароля."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Створює JWT-токен з даними користувача.
    У data можна передати {"sub": username, "role": "accountant"}.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or get_token_expiry())
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


