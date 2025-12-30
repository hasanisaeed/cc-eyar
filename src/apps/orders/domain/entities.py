from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class OrderEntity:
    product_name: str
    quantity: int
    total_price: int
    customer_id: int
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
