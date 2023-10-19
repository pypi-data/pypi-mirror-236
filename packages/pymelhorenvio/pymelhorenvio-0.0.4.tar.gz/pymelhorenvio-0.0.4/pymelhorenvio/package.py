from dataclasses import dataclass
from typing import Any, Dict, Iterable, List

from pymelhorenvio.freight_item import FreightItem

cm = float
kg = float


@dataclass
class Package:
    height: cm = 0.0
    width: cm = 0.0
    length: cm = 0.0
    weight: kg = 0.0

    def __post_init__(self) -> None:
        self.__items: Dict[FreightItem, List[FreightItem]] = {}

    def add_item(self, item: FreightItem) -> None:
        self.__calculate_package_dimensions(item)
        if item not in self.__items:
            self.__items[item] = []
        self.__items[item].append(item)

    def bulk_add_items(self, items: Iterable[FreightItem]) -> None:
        for item in items:
            self.add_item(item)

    def __calculate_package_dimensions(self, item: FreightItem) -> None:
        self.height += item.height
        self.width += item.width
        self.length += item.length
        self.weight += item.weight

    def asdict(self) -> Dict[str, Any]:
        return {
            "products": self.__get_products_asdict(),
            "package": self.__get_package_dimension_asdict(),
        }

    def __get_products_asdict(self) -> List[Dict[str, Any]]:
        return [
            {
                "width": item.width,
                "height": item.height,
                "length": item.length,
                "weight": item.weight,
                "insurance_value": item.insurance_value,
                "quantity": len(item_list),
            }
            for item, item_list in self.__items.items()
        ]

    def __get_package_dimension_asdict(self) -> Dict[str, Any]:
        return {
            "width": self.width,
            "height": self.height,
            "length": self.length,
            "weight": self.weight,
        }
