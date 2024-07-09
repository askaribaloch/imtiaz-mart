# app/db/models.py

from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, nullable=False, sa_column_kwargs={"unique": True})
    hashed_password: str = Field(nullable=False)
    full_name: str = Field(nullable=False)
    orders: List["Order"] = Relationship(back_populates="user")

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    price: float = Field(nullable=False)
    category: str = Field(nullable=False)
    stock: int = Field(nullable=False)

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    user: User = Relationship(back_populates="orders")
    is_paid: bool = Field(default=False)


class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id", nullable=False)
    product_id: int = Field(foreign_key="product.id", nullable=False)
    quantity: int = Field(nullable=False)
    price: float = Field(nullable=False)
    order: Order = Relationship(back_populates="items")