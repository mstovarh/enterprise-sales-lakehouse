from datetime import date

from sqlalchemy import BigInteger, Boolean, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = {"schema": "erp"}

    employee_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    store_id: Mapped[int] = mapped_column(
        ForeignKey("erp.stores.store_id"),
        nullable=False,
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

    job_title: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    hire_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )