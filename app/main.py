from fastapi import FastAPI, Depends
import psycopg2
import os
from dotenv import load_dotenv
from . import schemas, crud
from sqlalchemy.orm import Session
from app.database import get_db

# Load .env variables
load_dotenv()

app = FastAPI()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")


@app.on_event("startup")
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("✅ Successfully connected to PostgreSQL!")
        conn.close()
    except Exception as e:
        print("❌ Connection failed:", e)   


@app.get("/")
def root():
    return {"message": "FastAPI is running with PostgreSQL connection!"}

# Top Products
@app.get("/api/reports/top-products", response_model=list[schemas.ProductReport])
def get_top_products(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_top_products(db, limit)

# Channel Activity
@app.get("/api/channels/{channel_name}/activity", response_model=schemas.ChannelActivity)
def get_channel_activity(channel_name: str, db: Session = Depends(get_db)):
    return crud.get_channel_activity(db, channel_name)

# Search Messages
@app.get("/api/search/messages", response_model=list[schemas.Message])
def search_messages(query: str, db: Session = Depends(get_db)):
    return crud.search_messages(db, query)
