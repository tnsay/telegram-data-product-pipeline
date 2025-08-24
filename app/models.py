from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class FctMessages(Base):
    __tablename__ = "fct_messages"  # dbt model table
    message_id = Column(Integer, primary_key=True, index=True)
    channel_name = Column(String)
    message_text = Column(String)

class FctImageDetections(Base):
    __tablename__ = "fct_image_detections"
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer)
    detected_object_class = Column(String)
    confidence_score = Column(Float)
