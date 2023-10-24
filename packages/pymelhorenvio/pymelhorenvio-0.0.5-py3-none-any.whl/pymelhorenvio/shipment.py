from typing import Any, Dict, List, Union
from uuid import UUID

from pymelhorenvio.config import Config
from pymelhorenvio.freight_item import FreightItem
from pymelhorenvio.package import Package

try:
    from typing import Literal  # type: ignore
except ImportError:
    from typing_extensions import Literal  # type: ignore


class Shipment:
    def __init__(self, http_client, config: Config) -> None:
        self.__http_client = http_client
        self.__config = config

    def tracking(
        self, orders_id: List[Union[str, UUID]]
    ) -> Dict[str, Union[bool, int, float, str]]:
        url = f"{self.__config.get_base_url()}/api/v2/me/shipment/tracking"
        payload = {"orders": [*orders_id]}
        response = self.__http_client.post(
            url,
            headers=self.__config.get_headers(),
            json=payload,
        )
        items = response.json()
        self.__check_errors(items)
        return items

    def cancel(
        self, order_id: Union[str, UUID], description: str
    ) -> Dict[str, Union[bool, int, float, str]]:
        url = f"{self.__config.get_base_url()}/api/v2/me/shipment/cancel"
        payload = {
            "order": {
                "reason_id": "2",
                "id": f"{order_id}",
                "description": f"{description}",
            }
        }
        response = self.__http_client.post(
            url,
            headers=self.__config.get_headers(),
            json=payload,
        )
        items = response.json()
        self.__check_errors(items)
        return items

    def generate_tag(
        self, orders_id: List[Union[str, UUID]]
    ) -> Dict[str, Union[bool, int, float, str]]:
        url = f"{self.__config.get_base_url()}/api/v2/me/shipment/generate"
        payload = {"orders": [*orders_id]}
        response = self.__http_client.post(
            url,
            headers=self.__config.get_headers(),
            json=payload,
        )
        items = response.json()
        self.__check_errors(items)
        return items

    def print_tag(
        self,
        orders_id: List[Union[str, UUID]],
        mode: Literal["private", "public", ""] = "",
    ) -> Dict[str, Union[bool, int, float, str]]:
        url = f"{self.__config.get_base_url()}/api/v2/me/shipment/generate"
        payload: Dict[str, Any] = {"orders": [*orders_id]}
        default_modes = mode and self.print_tag.__defaults__
        if default_modes and mode in default_modes:
            payload["mode"] = mode
        response = self.__http_client.post(
            url,
            headers=self.__config.get_headers(),
            json=payload,
        )
        items = response.json()
        self.__check_errors(items)
        return items

    def preview_tag(
        self,
        orders_id: List[Union[str, UUID]],
    ) -> Dict[str, Union[bool, int, float, str]]:
        url = f"{self.__config.get_base_url()}/api/v2/me/shipment/preview"
        payload: Dict[str, Any] = {"orders": [*orders_id]}
        response = self.__http_client.post(
            url,
            headers=self.__config.get_headers(),
            json=payload,
        )
        items = response.json()
        self.__check_errors(items)
        return items

    def checkout(
        self, orders_id: List[Union[str, UUID]]
    ) -> Dict[str, Union[bool, int, float, str]]:
        url = f"{self.__config.get_base_url()}/api/v2/me/shipment/checkout"
        payload = {"orders": [*orders_id]}
        response = self.__http_client.post(
            url,
            headers=self.__config.get_headers(),
            json=payload,
        )
        items = response.json()
        self.__check_errors(items)
        return items

    def is_callable(
        self, orders_id: List[Union[str, UUID]]
    ) -> Dict[str, Union[bool, int, float, str]]:
        url = f"{self.__config.get_base_url()}/api/v2/me/shipment/cancellable"
        payload = {"orders": [*orders_id]}
        response = self.__http_client.post(
            url,
            headers=self.__config.get_headers(),
            json=payload,
        )
        items = response.json()
        self.__check_errors(items)
        return items

    def simulate_freight(
        self,
        cep_origin: str,
        cep_destin: str,
        height: int,
        width: int,
        length: int,
        weight: float,
        allowed_services: List[str] = [],
    ) -> Any:
        url = f"{self.__config.get_base_url()}/api/v2/me/shipment/calculate"
        item = FreightItem(height=height, width=width, length=length, weight=weight)
        package = Package()
        package.add_item(item)
        payload: Dict[str, Any] = {
            "from": {"postal_code": cep_origin},
            "to": {"postal_code": cep_destin},
            **package.asdict(),
        }
        allowed_services and payload.update({"services": ",".join(allowed_services)})
        response = self.__http_client.post(
            url,
            headers=self.__config.get_headers(),
            json=payload,
        )
        items = response.json()
        self.__check_errors(items)
        return items

    @staticmethod
    def __check_errors(items: Dict[str, Any]) -> None:
        if "errors" in items:
            raise ValueError(items.get("message", "No error message from provider API"))
