from datetime import date

from sqlalchemy import BigInteger, Boolean, Date, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Store(Base):
    __tablename__ = "stores"
    __table_args__ = {"schema": "erp"}

    store_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    store_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    region: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    channel: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    opened_at: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )