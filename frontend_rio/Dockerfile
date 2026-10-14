# Stage 1: builder
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Stage 2: runtime
FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /app /app

CMD ["python", "main.py"]
