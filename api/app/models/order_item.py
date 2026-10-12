from decimal import Decimal

from sqlalchemy import BigInteger, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = {"schema": "erp"}

    order_item_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("erp.orders.order_id", ondelete="CASCADE"),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("erp.products.product_id"),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )

    line_total: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    order: Mapped["Order"] = relationship(
        back_populates="items",
    )