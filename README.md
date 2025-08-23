# Telegram Data Product Pipeline

## Introduction
This project is developed at **Kara Solutions**, a leading data science company.  
Our task is to build a **robust data platform** that generates insights about **Ethiopian medical businesses**, using data scraped from public **Telegram channels**.

The pipeline integrates **scraping, data warehousing, transformations, enrichment with object detection, and an analytical API** to enable business insights.

---

## 🏢 Business Need
A well-designed data platform enhances data analysis and supports informed decisions.  
We aim to answer key business questions such as:

- **Top 10 medical products**: What are the most frequently mentioned drugs across channels?  
- 📊 **Price and availability trends**: How does a product vary across channels?  
- 🖼 **Visual content analysis**: Which channels have the most image-based posts (e.g., pills vs. creams)?  
- 📅 **Channel activity**: What are the daily and weekly posting trends?  

To solve this, we implement a **modern ELT framework**:

1. Extract raw data from Telegram → store in **Data Lake**.  
2. Load into **PostgreSQL Data Warehouse**.  
3. Transform with **dbt** into a **Star Schema** for analytics.  
4. Enrich with **YOLO object detection** for image data.  
5. Expose insights via an **Analytical API (FastAPI)**.  

---

## 🏗 Architecture

Telegram → Raw Data Lake → PostgreSQL (Warehouse) → dbt (Transformations)
→ YOLO (Image Enrichment) → Data Marts → FastAPI (Analytical API)

---

## ⚙️ Features
✅ **Data Scraping**: Telegram scraping with Telethon.  
✅ **Data Warehouse**: PostgreSQL with dimensional modeling (Star Schema).  
✅ **Data Transformation**: dbt for staging & marts layers.  
✅ **Image Enrichment**: YOLOv8 for object detection in media posts.  
✅ **Analytical API**: FastAPI to serve insights via endpoints.  
✅ **Orchestration**: Dagster for scheduling & monitoring.  
✅ **Secrets Management**: Environment variables for credentials.  

---

## 📂 Project Structure

telegram-data-product-pipeline/
├── data/ # Raw scraped data
│ └── raw/telegram_messages/
├── teledataproduct/ # dbt project (transformations, models, marts)
├── app/ # FastAPI analytical API
│ ├── main.py # FastAPI entrypoint
│ ├── database.py # DB connection
│ ├── models.py # SQLAlchemy models
│ ├── schemas.py # Pydantic schemas (validation)
│ └── crud.py # Query logic
├── dags/ # Dagster pipelines
├── requirements.txt # Python dependencies
├── docker-compose.yml # Services (db, API, orchestrator)
└── README.md # Project documentation
---

## 🚀 Setup Instructions

### 1️ Clone the repo
```bash
git clone https://github.com/your-org/telegram-data-product-pipeline.git
cd telegram-data-product-pipeline
```

### 2 Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```
### 3 Install dependencies
```bash
pip install -r requirements.txt
```
### 4 Set up environment variables

 Create a .env file at the project root:
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=telegram_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_SCHEMA=analytics
```
### 5 Run PostgreSQL with Docker
```bash
docker-compose up -d
```
### 6️ Run dbt models
```bash
cd teledataproduct
dbt run
dbt test
```
### 7 Start the API
```bash
uvicorn app.main:app --reload
```

#### API will be available at: http://127.0.0.1:8000

📡 API Endpoints

GET /api/reports/top-products?limit=10 → Most frequently mentioned products.

GET /api/channels/{channel_name}/activity → Posting activity of a channel.

GET /api/search/messages?query=paracetamol → Search messages by keyword.

🎯 Learning Outcomes
Skills

Telegram Data Extraction with Telethon
Data Modeling (Star Schema)
ELT Pipeline (Raw → Staging → Marts)
Dockerized Environments
Data Transformation with dbt
YOLO Object Detection for images
FastAPI for APIs
Dagster Orchestration
Secret Management with .env

Knowledge

-ELT vs ETL Architectures
-Layered Data Architecture (Data Lake → Staging → Marts)
-Data Cleaning & Validation Best Practices
-Dimensional Modeling for Analytics
-Integrating Structured & Unstructured Data
-Deploying & Maintaining Reproducible Data Pipelines

✅ Next Steps

Add monitoring & alerting for pipeline failures.

Deploy API & dbt jobs to cloud infrastructure.

Extend YOLO to detect more medical product types.

👩‍💻 Built with ❤️ TD