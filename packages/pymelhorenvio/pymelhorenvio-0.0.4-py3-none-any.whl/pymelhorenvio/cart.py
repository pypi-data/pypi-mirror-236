from typing import Any, Dict, Optional
from uuid import UUID

from pymelhorenvio.address import Address
from pymelhorenvio.config import Config
from pymelhorenvio.freight_item import FreightItem
from pymelhorenvio.receiver import Receiver
from pymelhorenvio.sender import Sender


class Cart:
    def __init__(
        self, http_client, config: Config, sender_class=Sender, receiver_class=Receiver
    ) -> None:
        self.__http_client = http_client
        self.__config = config
        self.__sender_class = sender_class
        self.__receiver_class = receiver_class

    def add_item(
        self,
        height,
        width,
        length,
        weight,
        sender_name: str,
        sender_phone: str,
        sender_email: str,
        sender_address: str,
        sender_complement: str,
        sender_number: str,
        sender_district: str,
        sender_city: str,
        sender_uf: str,
        sender_zipcode: str,
        sender_documentation: str,
        receiver_name: str,
        receiver_phone: str,
        receiver_email: str,
        receiver_address: str,
        receiver_complement: str,
        receiver_number: str,
        receiver_district: str,
        receiver_city: str,
        receiver_uf: str,
        receiver_zipcode: str,
        receiver_documentation: str,
        service_id: int,
    ) -> Optional[UUID]:
        url = f"{self.__config.get_base_url()}/api/v2/me/cart"
        item = FreightItem(height, width, length, weight, service=service_id)
        sender: Sender = self.__sender_class(sender_name, sender_phone, sender_email)
        sender.set_address(
            Address(
                address=sender_address,
                complement=sender_complement,
                number=sender_number,
                district=sender_district,
                city=sender_city,
                postal_code=sender_zipcode,
                state_abbr=sender_uf,
            )
        )
        sender.set_document(sender_documentation)
        receiver: Receiver = self.__receiver_class(
            receiver_name, receiver_phone, receiver_email
        )
        receiver.set_address(
            Address(
                address=receiver_address,
                complement=receiver_complement,
                number=receiver_number,
                district=receiver_district,
                city=receiver_city,
                postal_code=receiver_zipcode,
                state_abbr=receiver_uf,
            )
        )
        receiver.set_document(receiver_documentation)
        payload = {
            "from": sender.asdict(),
            "to": receiver.asdict(),
            "service": item.service,
            "volumes": [
                {
                    "height": height,
                    "width": width,
                    "length": length,
                    "weight": weight,
                }
            ],
            "options": {
                "receipt": True,
                "own_hand": True,
                "reverse": True,
                "non_commercial": True,
            },
        }
        response = self.__http_client.post(
            url, headers=self.__config.get_headers(), json=payload
        )
        items = response.json()
        self.__check_errors(items)
        return items

    def list_items(self) -> Any:
        url = f"{self.__config.get_base_url()}/api/v2/me/cart"
        response = self.__http_client.get(url, headers=self.__config.get_headers())
        items = response.json()
        self.__check_errors(items)
        return items

    def detail_item(self, order_id: str) -> Any:
        url = f"{self.__config.get_base_url()}/api/v2/me/cart/{order_id}"
        response = self.__http_client.get(url, headers=self.__config.get_headers())
        items = response.json()
        self.__check_errors(items)
        return items

    def remove_item(self, order_id: str) -> Any:
        url = f"{self.__config.get_base_url()}/api/v2/me/cart/{order_id}"
        response = self.__http_client.delete(url, headers=self.__config.get_headers())
        items = response.json()
        self.__check_errors(items)
        return items

    @staticmethod
    def __check_errors(items: Dict[str, Any]) -> None:
        if "errors" in items:
            raise ValueError(items.get("message", "No error message from provider API"))
