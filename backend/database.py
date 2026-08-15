from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# ⚙️ URL до БД: беремо з .env, якщо є, або дефолт для Docker
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:4568@rio_erp_db:5432/erp_diplom"
)

# 🔗 Engine для Postgres
engine = create_engine(DATABASE_URL)

# 🗂️ Сесії для роботи з БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 📦 Базовий клас для моделей
Base = declarative_base()

# ✅ Функція для отримання сесії (використовується у роутерах)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
