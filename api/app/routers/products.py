from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import (
    ProductSkuAlreadyExistsError,
    create_product,
    get_product_by_id,
    get_products,
)


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get("", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return get_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def retrieve_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = get_product_by_id(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_product(db, product_data)
    except ProductSkuAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A product with this SKU already exists",
        ) from exc