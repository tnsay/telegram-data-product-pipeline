import os

# Define folder and file structure
project_name = "."

folders = [
    f"{project_name}/app"
]

files = {
    f"{project_name}/.env": "",
    f"{project_name}/.gitignore": ".env\n__pycache__/\n*.pyc\n*.pyo\n",
    f"{project_name}/docker-compose.yml": """version: '3.8'

services:
  app:
    build: .
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
""",
    f"{project_name}/Dockerfile": """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app/main.py"]
""",
    f"{project_name}/requirements.txt": "python-dotenv\npsycopg2-binary\nSQLAlchemy\nrequests\n",
    f"{project_name}/README.md": "# Telegram Data Product Pipeline\n",
    f"{project_name}/app/__init__.py": ""
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files with content
for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Project structure '{project_name}' created successfully.")
