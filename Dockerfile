FROM python:3.11-slim

WORKDIR /app

# 빌드 도구 설치 (Postgres/MySQL 클라이언트 포함)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    default-libmysqlclient-dev \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 기본 실행 = uvicorn(FastAPI)
CMD ["uvicorn","src.main:app","--host","0.0.0.0","--port","8000"]