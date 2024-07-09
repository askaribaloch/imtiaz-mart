# app/schemas/payment.py

from pydantic import BaseModel

class PaymentCreate(BaseModel):
    card_number: str
    expiry_date: str
    cvv: str
