from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# ⚙️ Параметри БД з environment variables або дефолт для локального запуску
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "4568")
DB_NAME = os.getenv("DB_NAME", "erp_diplom")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
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
