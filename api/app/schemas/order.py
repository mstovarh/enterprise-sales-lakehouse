from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


OrderStatus = Literal[
    "CREATED",
    "PAID",
    "SHIPPED",
    "COMPLETED",
    "CANCELLED",
    "REFUNDED",
]

PaymentMethod = Literal[
    "CASH",
    "CREDIT_CARD",
    "DEBIT_CARD",
    "TRANSFER",
    "PSE",
]

SalesChannel = Literal[
    "STORE",
    "WEB",
    "MOBILE",
    "MARKETPLACE",
]


class OrderItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    discount_amount: Decimal = Field(default=0, ge=0)


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_item_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    discount_amount: Decimal
    line_total: Decimal


class OrderCreate(BaseModel):
    customer_id: int = Field(gt=0)
    store_id: int = Field(gt=0)
    employee_id: int | None = Field(default=None, gt=0)
    order_date: datetime | None = None
    order_status: OrderStatus = "CREATED"
    payment_method: PaymentMethod
    sales_channel: SalesChannel
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    customer_id: int
    store_id: int
    employee_id: int | None
    order_date: datetime
    order_status: OrderStatus
    payment_method: PaymentMethod
    sales_channel: SalesChannel
    subtotal_amount: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse]