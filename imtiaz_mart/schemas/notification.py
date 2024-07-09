# app/schemas/notification.py

from pydantic import BaseModel

class NotificationCreate(BaseModel):
    recipient: str
    message: str
