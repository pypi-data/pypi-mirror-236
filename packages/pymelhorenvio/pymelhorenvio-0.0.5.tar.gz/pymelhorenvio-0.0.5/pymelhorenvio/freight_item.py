from dataclasses import dataclass
from typing import Optional, Tuple, Union

from pymelhorenvio.freight_service import ShippingService


@dataclass(unsafe_hash=True)
class FreightItem:
    height: int
    width: int
    length: int
    weight: float
    service: Optional[ShippingService] = None
    insurance_value: float = 0

    def set_delivery_days(self, min: int, max: int) -> None:
        if not min or not max:
            return
        self.__min_delivery_days = min
        self.__max_delivery_days = max

    def get_delivery_range(self) -> Union[Tuple[int, int], Tuple]:
        return (
            all([self.__min_delivery_days, self.__max_delivery_days])
            and (self.__min_delivery_days, self.__max_delivery_days)
            or ()
        )
