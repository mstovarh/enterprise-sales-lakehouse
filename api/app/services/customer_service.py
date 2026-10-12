from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate


class CustomerEmailAlreadyExistsError(Exception):
    pass


def get_customers(db: Session) -> list[Customer]:
    statement = select(Customer).order_by(Customer.customer_id)

    return list(db.scalars(statement).all())


def get_customer_by_id(
    db: Session,
    customer_id: int,
) -> Customer | None:
    return db.get(Customer, customer_id)


def create_customer(
    db: Session,
    customer_data: CustomerCreate,
) -> Customer:
    customer = Customer(**customer_data.model_dump())

    db.add(customer)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise CustomerEmailAlreadyExistsError from exc

    db.refresh(customer)

    return customer