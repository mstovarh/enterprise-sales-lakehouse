from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


CustomerSegment = Literal[
    "REGULAR",
    "PREMIUM",
    "CORPORATE",
]


class CustomerCreate(BaseModel):
    first_name: str = Field(min_length=2, max_length=80)
    last_name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=30)
    city: str = Field(min_length=2, max_length=100)
    country: str = Field(default="Colombia", max_length=100)
    customer_segment: CustomerSegment = "REGULAR"


class CustomerResponse(CustomerCreate):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int
    created_at: datetime
    updated_at: datetime