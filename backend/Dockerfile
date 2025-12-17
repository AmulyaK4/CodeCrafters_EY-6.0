# backend/Dockerfile
FROM python:3.11-slim

ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Install system build deps needed by cryptography, mysql client, Pillow, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-dev libssl-dev libffi-dev rustc \
    libmariadb-dev libmariadb-dev-compat \
    libjpeg-dev zlib1g-dev libfreetype6-dev libxml2-dev libxslt1-dev \
    wget curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r /app/requirements.txt

# Copy whole repo so /app/backend exists
COPY . /app

# Keep WORKDIR at /app so "import backend" succeeds
WORKDIR /app

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

