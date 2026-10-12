from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"schema": "erp"}

    order_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("erp.customers.customer_id"),
        nullable=False,
    )

    store_id: Mapped[int] = mapped_column(
        ForeignKey("erp.stores.store_id"),
        nullable=False,
    )

    employee_id: Mapped[int | None] = mapped_column(
        ForeignKey("erp.employees.employee_id"),
        nullable=True,
    )

    order_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    order_status: Mapped[str] = mapped_column(String(30), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(30), nullable=False)
    sales_channel: Mapped[str] = mapped_column(String(30), nullable=False)

    subtotal_amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=0,
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=0,
    )

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=0,
    )

    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )