from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import get_db
from models import Product
from email_utils import send_low_stock_email

app = FastAPI(title="Inventory REST API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5000",
        "http://127.0.0.1:5000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProductIn(BaseModel):
    name: str = Field(..., min_length=1)
    stock: int = Field(..., ge=0)
    amount: int = Field(..., ge=0)


class ProductOut(ProductIn):
    id: int
    status: str

    class Config:
        from_attributes = True


def product_to_dict(product: Product):
    return {
        "id": product.id,
        "name": product.name,
        "stock": product.stock,
        "amount": product.amount,
        "status": "LOW STOCK" if product.stock <= product.amount * 0.25 else "OK",
    }


@app.get("/")
def home():
    return {"message": "Inventory API is running", "docs": "http://localhost:8000/docs"}


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).order_by(Product.id.asc()).all()
    return [product_to_dict(p) for p in products]


@app.post("/products", status_code=201)
def create_product(product: ProductIn, db: Session = Depends(get_db)):
    new_product = Product(name=product.name.strip(), stock=product.stock, amount=product.amount)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    if new_product.stock <= new_product.amount * 0.25:
        send_low_stock_email(new_product.name, new_product.stock, new_product.amount)

    return product_to_dict(new_product)


@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductIn, db: Session = Depends(get_db)):
    existing = db.query(Product).filter(Product.id == product_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")

    existing.name = product.name.strip()
    existing.stock = product.stock
    existing.amount = product.amount
    db.commit()
    db.refresh(existing)

    if existing.stock <= existing.amount * 0.25:
        send_low_stock_email(existing.name, existing.stock, existing.amount)

    return product_to_dict(existing)


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    existing = db.query(Product).filter(Product.id == product_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(existing)
    db.commit()
    return {"message": "Product deleted"}
