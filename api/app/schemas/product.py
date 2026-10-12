from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    sku: str = Field(min_length=2, max_length=50)
    product_name: str = Field(min_length=2, max_length=150)
    category: str = Field(min_length=2, max_length=80)
    brand: str = Field(min_length=2, max_length=80)
    unit_cost: Decimal = Field(ge=0)
    unit_price: Decimal = Field(gt=0)
    stock_quantity: int = Field(default=0, ge=0)
    is_active: bool = True


class ProductResponse(ProductCreate):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    created_at: datetime
    updated_at: datetime