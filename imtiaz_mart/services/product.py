# app/services/product.py

from fastapi import HTTPException, Depends
from sqlmodel import Session, select
from app.db.models import Product
from app.schemas.product import ProductCreate, ProductRead
from app.services.user import get_current_user

def get_product(db: Session, product_id: int):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def get_products(db: Session):
    products = db.exec(select(Product)).all()
    return products

def create_product(db: Session, product: ProductCreate, current_user: User = Depends(get_current_user)):
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Implement other CRUD operations for products
