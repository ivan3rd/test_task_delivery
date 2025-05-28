FROM python:3.13

WORKDIR /backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt


COPY ./ /backend

# Environment variables (can also be set in compose file)
ENV PYTHONPATH=/app

CMD ["sh", "-c", "\

  echo 'Waiting for MySQL...' && \
  until mysqladmin ping -h db -u ${MYSQL_USER} -p${MYSQL_PASSWORD} --silent; do sleep 2; done && \
  echo 'Running migrations...' && \
  alembic upgrade head && \
  echo 'Loading pre production data...' && \
  /bin/bash ./load_database.sh && \
  echo 'Starting FastAPI...' && \
  watchfiles 'uvicorn app.main:app --host 0.0.0.0 --port 8000' \
"]
