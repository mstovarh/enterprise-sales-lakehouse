from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import (
    DuplicatedProductError,
    InsufficientStockError,
    OrderReferenceError,
    create_order,
    get_order_by_id,
    get_orders,
)


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.get("", response_model=list[OrderResponse])
def list_orders(
    db: Session = Depends(get_db),
):
    return get_orders(db)


@router.get("/{order_id}", response_model=OrderResponse)
def retrieve_order(
    order_id: int,
    db: Session = Depends(get_db),
):
    order = get_order_by_id(db, order_id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return order


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_order(db, order_data)

    except OrderReferenceError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except DuplicatedProductError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except InsufficientStockError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc