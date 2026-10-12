from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = {"schema": "erp"}

    customer_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="Colombia",
    )

    customer_segment: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="REGULAR",
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