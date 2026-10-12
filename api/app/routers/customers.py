from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services.customer_service import (
    CustomerEmailAlreadyExistsError,
    create_customer,
    get_customer_by_id,
    get_customers,
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.get(
    "",
    response_model=list[CustomerResponse],
)
def list_customers(
    db: Session = Depends(get_db),
) -> list[CustomerResponse]:
    return get_customers(db)


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def retrieve_customer(
    customer_id: int,
    db: Session = Depends(get_db),
) -> CustomerResponse:
    customer = get_customer_by_id(db, customer_id)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return customer


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
) -> CustomerResponse:
    try:
        return create_customer(db, customer_data)
    except CustomerEmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A customer with this email already exists",
        ) from exc