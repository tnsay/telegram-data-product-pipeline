from pydantic import BaseModel
from datetime import datetime

class MessageSchema(BaseModel):
    message_id: int
    channel_name: str
    message_text: str
    created_at: datetime

    class Config:
        orm_mode = True

class DetectionSchema(BaseModel):
    message_id: int
    detected_object_class: str
    confidence_score: float

    class Config:
        orm_mode = True
