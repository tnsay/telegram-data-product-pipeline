import os
import json
from dotenv import load_dotenv
import psycopg2
from datetime import datetime

# Path to raw scraped data
BASE_DIR = "../data/raw/telegram_messages"

load_dotenv()

# Read credentials from .env
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Connect to Postgres
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()
print("✅ Connected to database successfully!")

# Ensure schema & table exist
cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
cur.execute("""
CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    id BIGINT,
    channel TEXT,
    date_val TIMESTAMP,
    sender_id BIGINT,
    message TEXT,
    has_media BOOLEAN,
    media_path TEXT,
    PRIMARY KEY (channel, id)
);
""")

# Iterate through folders: date → channel
for date_folder in os.listdir(BASE_DIR):
    date_path = os.path.join(BASE_DIR, date_folder)

    if not os.path.isdir(date_path):
        continue  # skip non-directories

    for channel in os.listdir(date_path):
        file_path = os.path.join(date_path, channel, f"{channel}_messages.json")

        if not os.path.exists(file_path):
            print(f"⚠️ Skipping missing file: {file_path}")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            try:
                messages = json.load(f)
            except json.JSONDecodeError:
                print(f"⚠️ Invalid JSON in {file_path}, skipping...")
                continueC

        inserted = 0
        for msg in messages:
            try:
                # Parse date
                date_str = msg.get("date")
                date_val = None
                if date_str:
                    try:
                        date_val = datetime.fromisoformat(date_str)
                    except ValueError:
                        try:
                            date_val = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                        except Exception:
                            pass

                # Parse sender safely
                sender_id = None
                from_id = msg.get("from_id")
                if isinstance(from_id, dict):
                    sender_id = from_id.get("user_id")


                media_path = msg.get("downloaded_media_path")
                # if not media_path and msg.get("media"):
                #     media_path = os.path.join(date_path, channel, "media", f"{msg['id']}.jpg") 


                cur.execute("""
                INSERT INTO raw.telegram_messages 
                    (id, channel, date_val, sender_id, message, has_media, media_path)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (channel, id) DO NOTHING;
                """, (
                    msg.get("id"),
                    channel,
                    date_val,
                    sender_id,
                    msg.get("message"),
                    True if msg.get("media") else False,
                    media_path
                ))
                inserted += 1
            except Exception as e:
                print(f"⚠️ Failed to insert message {msg.get('id')}: {e}")

        print(f"✅ {inserted} messages loaded for channel {channel} ({date_folder})")

conn.commit()

# Optional: add indexes for dbt performance
cur.execute("CREATE INDEX IF NOT EXISTS idx_channel_date ON raw.telegram_messages (channel, date_val);")

cur.close()
conn.close()
print("🎯 All raw messages loaded into Postgres (schema=raw)")













# import os
# import json
# from dotenv import load_dotenv
# import psycopg2
# from psycopg2.extras import Json
# from datetime import datetime


# RAW_PATH = "../data/raw/telegram_messages/2025-08-19"
# CHANNELS = ["CheMed123", "lobelia4cosmetics", "tikvahpharma"]

# load_dotenv()

# # Read credentials from .env
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_HOST = os.getenv("DB_HOST", "localhost")  # default localhost
# DB_PORT = os.getenv("DB_PORT", "5432")       # default 5432

# conn = psycopg2.connect(
#     dbname=DB_NAME,
#     user=DB_USER,
#     password=DB_PASSWORD,
#     host=DB_HOST,
#     port=DB_PORT
# )

# cur = conn.cursor()
# print("✅ Connected to database successfully!")

# # Create raw table
# try:
#     cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS raw.telegram_messages (
#         id BIGINT PRIMARY KEY,
#         channel TEXT,
#         date_val TIMESTAMP,
#         sender_id BIGINT,
#         message TEXT,
#         has_media BOOLEAN,
#         media_path TEXT
#     );
#     """)
# except Exception as e:
#     print(f"⚠️ Skipped message {msg.get('id')} due to error: {e}")

# # Iterate through JSON files
# base_dir = "../data/raw/telegram_messages"
# for date_folder in os.listdir(base_dir):
#     date_path = os.path.join(base_dir, date_folder)
#     for channel in os.listdir(date_path):
#         file_path = os.path.join(date_path, channel, "messages.json")
#         with open(file_path, "r", encoding="utf-8") as f:
#             messages = json.load(f)

# date_str = msg.get("date")
#                 date_val = None
#                 if date_str:
#                     try:
#                         date_val = datetime.fromisoformat(date_str)
#                     except ValueError:
#                         pass  # leave as None if malformed

#         for msg in messages:
#             cur.execute("""
#             INSERT INTO raw.telegram_messages (id, channel, date_val, sender_id, message, has_media, media_path)
#             VALUES (%s, %s, %s, %s, %s, %s, %s)
#             ON CONFLICT (id) DO NOTHING;
#             """, (
#                 msg.get("id"),
#                 channel,
#                 date_val,             
#                 date_str = msg.get("date"),
#                 date_val = datetime.fromisoformat(date_str) if date_str else None,
#                 msg.get("from_id", {}).get("user_id") if msg.get("from_id") else None,
#                 msg.get("message"),
#                 True if msg.get("media") else False,
#                 msg.get("downloaded_media_path")
#             ))

# conn.commit()
# cur.close()
# conn.close()
# print("✅ Raw messages loaded into Postgres (schema=raw)")