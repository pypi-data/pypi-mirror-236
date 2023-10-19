from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Union


@dataclass(frozen=True)
class ShippingCompany:
    name: str
    image: str = ""
    id: Optional[int] = None


@dataclass
class ShippingService:
    name: str
    price: Union[Decimal, float]
    company: ShippingCompany
    id: Optional[int] = None
