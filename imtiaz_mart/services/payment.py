# app/services/payment.py

from fastapi import HTTPException, Depends
from sqlmodel import Session
from app.db.models import Order
from app.schemas.payment import PaymentCreate
from app.services.order import get_order

# Implement a mock payment processing function
def process_payment(payment: PaymentCreate):
    # Perform payment processing logic
    # ...
    return True

def pay_for_order(db: Session, order_id: int, payment: PaymentCreate):
    order = get_order(db, order_id)
    if order.is_paid:
        raise HTTPException(status_code=400, detail="Order is already paid")

    if process_payment(payment):
        order.is_paid = True
        db.commit()
        db.refresh(order)
        return order
    else:
        raise HTTPException(status_code=400, detail="Payment failed")
