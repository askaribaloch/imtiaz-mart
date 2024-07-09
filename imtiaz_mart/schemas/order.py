# app/schemas/order.py

from typing import List
from pydantic import BaseModel

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderItemRead(OrderItemCreate):
    id: int
    price: float

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    items: List[OrderItemCreate]

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int
    user_id: int
    is_paid: bool
    items: List[OrderItemRead]

    class Config:
        orm_mode = True
