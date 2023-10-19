from typing import Any, Dict, Union
from uuid import UUID

from pymelhorenvio.config import Config

try:
    from typing import Literal  # type: ignore
except ImportError:
    from typing_extensions import Literal  # type: ignore


ALLOWED_STATUS = Literal[
    "Pending",
    "Released",
    "Posted",
    "Delivered",
    "Cancelled",
    "Not Delivered",
    "",
    "pending",
    "released",
    "posted",
    "delivered",
    "cancelled",
    "not delivered",
]


class Order:
    def __init__(self, http_client, config: Config) -> None:
        self.__http_client = http_client
        self.__config = config

    def search(
        self, q: Union[str, UUID], status: ALLOWED_STATUS = ""
    ) -> Dict[str, Union[bool, int, float, str]]:
        url = f"{self.__config.get_base_url()}/api/v2/me/orders/search?q={q}"
        if status:
            url = f"{url}&status={status}"
        response = self.__http_client.get(
            url,
            headers=self.__config.get_headers(),
        )
        items = response.json()
        self.__check_errors(items)
        return items

    def list(
        self, status: ALLOWED_STATUS = ""
    ) -> Dict[str, Union[bool, int, float, str]]:
        url = f"{self.__config.get_base_url()}/api/v2/me/orders?status={status}"
        response = self.__http_client.get(
            url,
            headers=self.__config.get_headers(),
        )
        items = response.json()
        self.__check_errors(items)
        return items

    def detail(
        self, order_id: Union[str, UUID]
    ) -> Dict[str, Union[bool, int, float, str]]:
        url = f"{self.__config.get_base_url()}/api/v2/me/orders/{order_id}"
        response = self.__http_client.get(
            url,
            headers=self.__config.get_headers(),
        )
        items = response.json()
        self.__check_errors(items)
        return items

    @staticmethod
    def __check_errors(items: Dict[str, Any]) -> None:
        if "errors" in items:
            raise ValueError(items.get("message", "No error message from provider API"))
