import httpx

from pymelhorenvio.account import Account
from pymelhorenvio.cart import Cart
from pymelhorenvio.config import Config
from pymelhorenvio.order import Order
from pymelhorenvio.shipment import Shipment


class MelhorEnvio:
    def __init__(
        self, use_sandbox: bool = True, token: str = "", http_client=httpx
    ) -> None:
        self.__config = Config(use_sandbox=use_sandbox, token=token)
        self.__http_client = http_client

    def get_environ(self) -> str:
        return self.__config.get_base_url()

    @property
    def shipment(self) -> Shipment:
        return Shipment(http_client=self.__http_client, config=self.__config)

    @property
    def cart(self) -> Cart:
        return Cart(http_client=self.__http_client, config=self.__config)

    @property
    def order(self) -> Order:
        return Order(http_client=self.__http_client, config=self.__config)

    @property
    def account(self) -> Account:
        return Account(http_client=self.__http_client, config=self.__config)
