# db/crud/product.py


from sqlalchemy.orm import Session

from app.models.product import Product


def get_product_by_name(db: Session, name: str):
    return db.query(Product).filter(Product.name == name).first()


def get_product_by_id(db: Session, id: int):
    return db.query(Product).filter(Product.id == id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: Product):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
