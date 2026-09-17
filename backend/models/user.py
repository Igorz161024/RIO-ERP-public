from sqlalchemy import Column, Integer, String
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    # 🔑 Нові поля
    role = Column(String, default="user", nullable=False)          # роль користувача (admin, user, auditor)
    refresh_token = Column(String, nullable=True)                  # refresh‑токен для оновлення access‑токена
