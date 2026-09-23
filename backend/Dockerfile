FROM python:3.12-slim

WORKDIR /app

# Копіюємо тільки requirements.txt для кешування залежностей
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту
COPY . .

# Запускаємо FastAPI через Uvicorn
# За замовчуванням бекенд слухає порт 7000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7000"]
