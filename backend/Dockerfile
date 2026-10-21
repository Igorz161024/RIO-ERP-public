# Stage 1: builder
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Копіюємо requirements.txt з backend
COPY backend/requirements.txt backend-requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r backend-requirements.txt

COPY . .

# Stage 2: runtime
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Копіюємо встановлені пакети з builder-шару
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

ENV PATH="/usr/local/bin:${PATH}"
ENV PYTHONPATH=/app

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7000"]