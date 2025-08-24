from sqlalchemy.orm import Session
from . import models

# 1. Top products
def get_top_products(db: Session, limit: int = 10):
    return (
        db.query(models.FctImageDetections.detected_object_class)
        .group_by(models.FctImageDetections.detected_object_class)
        .order_by(db.func.count().desc())
        .limit(limit)
        .all()
    )

# 2. Channel activity
def get_channel_activity(db: Session, channel_name: str):
    return (
        db.query(models.FctMessages)
        .filter(models.FctMessages.channel_name == channel_name)
        .all()
    )

# 3. Search messages
def search_messages(db: Session, query: str):
    return (
        db.query(models.FctMessages)
        .filter(models.FctMessages.message_text.ilike(f"%{query}%"))
        .all()
    )
