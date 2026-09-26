import os

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60*24*365))

# Database settings
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "4568")
POSTGRES_DB = os.getenv("POSTGRES_DB", "erp_diplom")
DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@erp_db:5432/{POSTGRES_DB}")

DEBUG = os.getenv("DEBUG", "True") == "True"
