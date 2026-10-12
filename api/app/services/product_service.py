from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate


class ProductSkuAlreadyExistsError(Exception):
    pass


def get_products(db: Session) -> list[Product]:
    statement = select(Product).order_by(Product.product_id)
    return list(db.scalars(statement).all())


def get_product_by_id(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)


def create_product(db: Session, product_data: ProductCreate) -> Product:
    product = Product(**product_data.model_dump())
    db.add(product)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ProductSkuAlreadyExistsError from exc

    db.refresh(product)
    return product