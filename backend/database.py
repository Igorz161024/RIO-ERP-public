from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# 🔑 Завантажуємо саме .env.prod
load_dotenv(".env.prod")

# ⚙️ URL до БД з .env.prod
DATABASE_URL = os.getenv("DATABASE_URL")

# 🔗 Якщо змінна не задана, беремо дефолт для локального запуску
if not DATABASE_URL:
    DATABASE_URL = "postgresql+psycopg2://postgres:4568@localhost:5433/erp_diplom"

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
