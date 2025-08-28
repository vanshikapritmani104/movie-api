# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# System deps for SQLite
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential sqlite3 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY .env ./.env

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]