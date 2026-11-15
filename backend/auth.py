import os
from dotenv import load_dotenv
from datetime import timedelta, datetime
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.database import get_db

# -------------------------------
# Завантаження змінних середовища
# -------------------------------
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "change_me")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "525600")
)

REFRESH_TOKEN_EXPIRE_DAYS = 30

# -------------------------------
# Конфігурація bcrypt
# -------------------------------
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# -------------------------------
# OAuth2
# -------------------------------
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)

# -------------------------------
# Паролі
# -------------------------------
def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def get_password_hash(
    password: str
) -> str:
    return pwd_context.hash(password)


# -------------------------------
# Аутентифікація
# -------------------------------
def authenticate_user(
    db: Session,
    username: str,
    password: str
):
    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash
    ):
        return None

    return user


# -------------------------------
# JWT токени
# -------------------------------
def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:

    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta
        or timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def create_refresh_token(
    user: User
) -> str:

    expire = datetime.utcnow() + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    to_encode = {
        "sub": user.username,
        "role": user.role,
        "exp": expire
    }

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


# -------------------------------
# Поточний користувач
# -------------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:

    payload = verify_token(token)

    username = payload.get("sub")

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not found in token"
        )

    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


def get_current_user_role(
    token: str = Depends(oauth2_scheme)
) -> str:

    payload = verify_token(token)

    role = payload.get("role")

    if role is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Role not found in token"
        )

    return role