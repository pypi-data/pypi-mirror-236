from typing import Any, Dict, Optional
from uuid import UUID

from pymelhorenvio.config import Config


class Account:
    def __init__(self, http_client, config: Config) -> None:
        self.__http_client = http_client
        self.__config = config

    def get_balace(self) -> Optional[UUID]:
        url = f"{self.__config.get_base_url()}/api/v2/me/balance"
        response = self.__http_client.get(url, headers=self.__config.get_headers())
        items = response.json()
        self.__check_errors(items)
        return items

    @staticmethod
    def __check_errors(items: Dict[str, Any]) -> None:
        if "errors" in items:
            raise ValueError(items.get("message", "No error message from provider API"))
