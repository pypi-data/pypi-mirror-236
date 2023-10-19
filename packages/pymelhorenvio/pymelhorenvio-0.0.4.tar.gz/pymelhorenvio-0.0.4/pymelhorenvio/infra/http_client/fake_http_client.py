from typing import Any, Dict, List, Union


class FakeHttpClient:
    def __init__(
        self, output: Union[Dict[str, Any], List[Dict[str, Any]]] = {}
    ) -> None:
        self.__output = output

    def json(self) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        return self.__output or {}

    def post(self, *args, **kwargs) -> "FakeHttpClient":
        return self
