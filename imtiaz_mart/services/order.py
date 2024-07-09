# app/services/order.py

from fastapi import HTTPException, Depends
from sqlmodel import Session, select
from app.db.models import Order, OrderItem
from app.schemas.order import OrderCreate, OrderRead
from app.services.user import get_current_user
from app.services.product import get_product

def get_order(db: Session, order_id: int):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def get_orders(db: Session, current_user: User = Depends(get_current_user)):
    orders = db.exec(select(Order).where(Order.user_id == current_user.id)).all()
    return orders

def create_order(db: Session, order: OrderCreate, current_user: User = Depends(get_current_user)):
    order_items = []
    for item in order.items:
        product = get_product(db, item.product_id)
        order_item = OrderItem(product_id=product.id, quantity=item.quantity, price=product.price)
        order_items.append(order_item)

    db_order = Order(user_id=current_user.id, items=order_items)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# Implement other CRUD operations for orders
