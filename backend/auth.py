import os
from dotenv import load_dotenv
from datetime import timedelta

# Завантаження секретів
load_dotenv(dotenv_path=".env.prod")

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey123")
ALGORITHM = "HS256"

# час життя токена у хвилинах (1 рік)
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365
REFRESH_TOKEN_EXPIRE_DAYS = 7

def get_token_expiry():
    return timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


