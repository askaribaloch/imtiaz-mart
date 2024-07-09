# app/main.py

from fastapi import FastAPI, Depends
from sqlmodel import Session, create_engine
from app.db.models import User, Product, Order
from app.services.auth import authenticate_user, create_user
from app.services.product import get_products, create_product
from app.services.order import get_orders, create_order
from app.services.payment import pay_for_order
from app.services.notification import notify_order_status
from app.schemas.auth import UserCreate, UserRead
from app.schemas.product import ProductCreate
from app.schemas.order import OrderCreate
from app.schemas.payment import PaymentCreate
from app.schemas.notification import NotificationCreate

app = FastAPI()

# Database setup
engine = create_engine("sqlite:///./imtiaz_mart.db")

# Dependency
def get_db():
    with Session(engine) as session:
        yield session

# Authentication routes
@app.post("/auth/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@app.post("/auth/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    user = authenticate_user(db, user.email, user.password)
    # Generate and return JWT token

# Product routes
@app.get("/products", response_model=List[ProductRead])
def get_all_products(db: Session = Depends(get_db)):
    return get_products(db)

@app.post("/products", response_model=ProductRead)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_product(db, product, current_user)

# Order routes
@app.get("/orders", response_model=List[OrderRead])
def get_user_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_orders(db, current_user)

@app.post("/orders", response_model=OrderRead)
def create_new_order(order: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_order(db, order, current_user)

# Payment routes
@app.post("/orders/{order_id}/pay", response_model=OrderRead)
def pay_for_order_route(order_id: int, payment: PaymentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return pay_for_order(db, order_id, payment)

# Notification routes
@app.post("/orders/{order_id}/notify", response_model=OrderRead)
def order_id_notification(order_id: int, notification: NotificationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return notify_order_status(db, order_id, notification)