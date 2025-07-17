FROM python:3.11-slim

# Install system dependencies first (for psycopg2, pandas, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Use a virtual environment (optional but cleaner)
WORKDIR /app

# Install Python deps first (use caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then copy your application
COPY . .

CMD ["python", "app/main.py"]
