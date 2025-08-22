import os
import sys
import hashlib
from datetime import datetime
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

# YOLO
from ultralytics import YOLO

# ------------ Config ------------
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}  # handle images only
YOLO_MODEL = os.getenv("YOLO_MODEL", "yolov8n.pt")       # can override in .env
BATCH_SIZE = 1                                           # 1-by-1 is OK on CPU
# --------------------------------

def abspath_from_media_path(media_path: str) -> str:
    """
    Make the relative path (as stored in DB) absolute, robust on Windows/*nix.
    We resolve relative to this script's directory.
    """
    if not media_path:
        return None
    script_dir = Path(__file__).resolve().parent
    # Normalize .. and slashes
    p = (script_dir / media_path).resolve()
    return str(p)

def file_sha1(path: str) -> str:
    """Hash file bytes to identify exact media content."""
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    load_dotenv()

    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )
    cur = conn.cursor()
    print("✅ Connected to database")

    # 1) Ensure raw table exists
    cur.execute("""
    CREATE SCHEMA IF NOT EXISTS raw;

    CREATE TABLE IF NOT EXISTS raw.image_detections (
        detection_id        BIGSERIAL PRIMARY KEY,
        message_id          BIGINT NOT NULL,
        media_path          TEXT NOT NULL,
        media_sha1          TEXT NOT NULL,
        detected_object_class TEXT NOT NULL,
        confidence_score    NUMERIC(5,3) NOT NULL,
        yolo_model          TEXT NOT NULL,
        run_ts              TIMESTAMPTZ NOT NULL DEFAULT now(),
        UNIQUE (message_id, media_sha1, detected_object_class, confidence_score, yolo_model)
    );
    """)
    conn.commit()

    # 2) Fetch candidate images from raw.telegram_messages
    #    Only those that claim to have media AND have a non-null path
    cur.execute("""
    SELECT id AS message_id, media_path
    FROM raw.telegram_messages
    WHERE has_media = TRUE
      AND media_path IS NOT NULL
    """)
    rows = cur.fetchall()
    print(f"🔎 Found {len(rows)} messages with media to check")

    # 3) Load YOLO
    print(f"📦 Loading YOLO model: {YOLO_MODEL}")
    model = YOLO(YOLO_MODEL)

    inserted = 0
    skipped_missing = 0
    skipped_not_image = 0
    already_had = 0
    errors = 0

    for (message_id, media_path) in rows:
        abs_path = abspath_from_media_path(media_path)
        if not abs_path or not os.path.exists(abs_path):
            skipped_missing += 1
            continue

        ext = Path(abs_path).suffix.lower()
        if ext not in IMAGE_EXTS:
            # For now we only handle images (skip videos)
            skipped_not_image += 1
            continue

        try:
            # hash the file to make de-dupe idempotent
            sha1 = file_sha1(abs_path)

            # Optional: skip if detections already exist for this (message_id, sha1, model)
            cur.execute("""
            SELECT 1
            FROM raw.image_detections
            WHERE message_id = %s
              AND media_sha1 = %s
              AND yolo_model = %s
            LIMIT 1
            """, (message_id, sha1, YOLO_MODEL))
            if cur.fetchone():
                already_had += 1
                continue

            # 4) Run YOLO
            results = model(abs_path, verbose=False)

            # 5) Insert detections
            # YOLO returns one result per image here
            for r in results:
                if not hasattr(r, "boxes") or r.boxes is None:
                    continue
                names = r.names  # id -> class name
                for b in r.boxes:
                    # some tensors need .item() to become python scalars
                    cls_id = int(b.cls[0].item() if hasattr(b.cls[0], "item") else b.cls[0])
                    conf = float(b.conf[0].item() if hasattr(b.conf[0], "item") else b.conf[0])
                    class_name = str(names[cls_id]).lower().strip()

                    cur.execute("""
                    INSERT INTO raw.image_detections
                        (message_id, media_path, media_sha1, detected_object_class, confidence_score, yolo_model, run_ts)
                    VALUES (%s, %s, %s, %s, %s, %s, now())
                    ON CONFLICT DO NOTHING
                    """, (message_id, media_path, sha1, class_name, round(conf, 3), YOLO_MODEL))
                    inserted += 1

            conn.commit()

        except Exception as e:
            errors += 1
            conn.rollback()
            print(f"⚠️ Error on message_id={message_id}: {e}", file=sys.stderr)

    cur.close()
    conn.close()

    print("---- Summary ----")
    print(f"✅ Inserted detections : {inserted}")
    print(f"↩️  Already existed    : {already_had}")
    print(f"🖼️  Skipped non-images : {skipped_not_image}")
    print(f"❓  Missing files      : {skipped_missing}")
    print(f"💥 Errors             : {errors}")

if __name__ == "__main__":
    main()
