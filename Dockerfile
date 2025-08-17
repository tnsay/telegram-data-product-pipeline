# Stage 1: Builder (heavy image with compilers, builds deps once)
FROM python:3.11 as builder

# Install build tools + headers
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip for better wheel support
RUN pip install --upgrade pip setuptools wheel

WORKDIR /app

# Install dependencies into a separate directory
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
 && pip install --no-cache-dir --prefix=/install -r requirements.txt



# Stage 2: Final runtime (slim + only runtime libs)
FROM python:3.11-slim

# Install runtime system packages only (no compilers here!)
RUN apt-get update && apt-get install -y \
    libpq5 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed python packages from builder
COPY --from=builder /install /usr/local

# Copy project code
COPY . .

# Make wait script executable
RUN chmod +x wait-for-db.sh

# Default command
CMD ["python", "app/main.py"]

















# FROM python:3.11-slim

# # Install system dependencies for psycopg2 and other packages
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libpq-dev \
#     build-essential \
#     postgresql-client \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# # Install Python dependencies first for caching
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the wait script and app code
# COPY wait-for-db.sh .
# COPY . .

# # Make wait script executable
# RUN chmod +x wait-for-db.sh

# # Default command (will be overridden by docker-compose)
# CMD ["python", "app/main.py"]



















# # FROM python:3.11-slim

# # # python envt containarized
# # # Install system dependencies first (for psycopg2- to talk to postgress, pandas, etc.)
# # RUN apt-get update && apt-get install -y \
# #     gcc \
# #     libpq-dev \
# #     build-essential \
# #     && rm -rf /var/lib/apt/lists/*

# # # Use a virtual environment/set working directory app
# # WORKDIR /app

# # # Install Python deps first (using caching)
# # COPY requirements.txt .
# # RUN pip install --no-cache-dir -r requirements.txt

# # # Then copy your application
# # COPY . .

# # # runs when docker starts
# # CMD ["python", "app/main.py"]  
