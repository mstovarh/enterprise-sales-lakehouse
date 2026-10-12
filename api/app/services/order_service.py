from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.customer import Customer
from app.models.employee import Employee
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.store import Store
from app.schemas.order import OrderCreate


TAX_RATE = Decimal("0.19")


class OrderReferenceError(Exception):
    pass


class InsufficientStockError(Exception):
    pass


class DuplicatedProductError(Exception):
    pass


def get_orders(db: Session) -> list[Order]:
    statement = (
        select(Order)
        .options(selectinload(Order.items))
        .order_by(Order.order_id)
    )

    return list(db.scalars(statement).all())


def get_order_by_id(
    db: Session,
    order_id: int,
) -> Order | None:
    statement = (
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.order_id == order_id)
    )

    return db.scalar(statement)


def create_order(
    db: Session,
    order_data: OrderCreate,
) -> Order:
    customer = db.get(Customer, order_data.customer_id)

    if customer is None:
        raise OrderReferenceError("Customer does not exist")

    store = db.get(Store, order_data.store_id)

    if store is None:
        raise OrderReferenceError("Store does not exist")

    if order_data.employee_id is not None:
        employee = db.get(Employee, order_data.employee_id)

        if employee is None:
            raise OrderReferenceError("Employee does not exist")

        if employee.store_id != order_data.store_id:
            raise OrderReferenceError(
                "Employee does not belong to the selected store"
            )

    product_ids = [item.product_id for item in order_data.items]

    if len(product_ids) != len(set(product_ids)):
        raise DuplicatedProductError(
            "The same product cannot appear twice in one order"
        )

    try:
        order = Order(
            customer_id=order_data.customer_id,
            store_id=order_data.store_id,
            employee_id=order_data.employee_id,
            order_date=order_data.order_date or datetime.utcnow(),
            order_status=order_data.order_status,
            payment_method=order_data.payment_method,
            sales_channel=order_data.sales_channel,
            subtotal_amount=Decimal("0.00"),
            discount_amount=Decimal("0.00"),
            tax_amount=Decimal("0.00"),
            total_amount=Decimal("0.00"),
        )

        db.add(order)
        db.flush()

        subtotal = Decimal("0.00")
        total_discount = Decimal("0.00")

        for requested_item in order_data.items:
            product = db.get(Product, requested_item.product_id)

            if product is None:
                raise OrderReferenceError(
                    f"Product {requested_item.product_id} does not exist"
                )

            if not product.is_active:
                raise OrderReferenceError(
                    f"Product {product.product_id} is inactive"
                )

            if product.stock_quantity < requested_item.quantity:
                raise InsufficientStockError(
                    f"Insufficient stock for product {product.sku}. "
                    f"Available: {product.stock_quantity}"
                )

            gross_amount = (
                product.unit_price * requested_item.quantity
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            if requested_item.discount_amount > gross_amount:
                raise OrderReferenceError(
                    f"Discount exceeds the value of product {product.sku}"
                )

            line_total = (
                gross_amount - requested_item.discount_amount
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            order_item = OrderItem(
                order_id=order.order_id,
                product_id=product.product_id,
                quantity=requested_item.quantity,
                unit_price=product.unit_price,
                discount_amount=requested_item.discount_amount,
                line_total=line_total,
            )

            db.add(order_item)

            product.stock_quantity -= requested_item.quantity

            subtotal += gross_amount
            total_discount += requested_item.discount_amount

        taxable_amount = subtotal - total_discount

        tax_amount = (taxable_amount * TAX_RATE).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        total_amount = taxable_amount + tax_amount

        order.subtotal_amount = subtotal
        order.discount_amount = total_discount
        order.tax_amount = tax_amount
        order.total_amount = total_amount

        db.commit()

    except Exception:
        db.rollback()
        raise

    return get_order_by_id(db, order.order_id)