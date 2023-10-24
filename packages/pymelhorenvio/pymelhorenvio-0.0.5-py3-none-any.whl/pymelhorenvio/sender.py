import re
from dataclasses import dataclass
from typing import Optional

from pymelhorenvio.address import Address


@dataclass
class Sender:
    name: str
    phone: str
    email: str

    def __post_init__(self) -> None:
        self.__address: Optional[Address] = None
        self.__document: str = ""
        self.__company_document: str = ""

    def set_document(self, document: str, state_register: str = "") -> None:
        document_as_digits = re.sub("\D", "", document)
        if len(document_as_digits) < 11 or len(document_as_digits) > 14:
            raise ValueError(f"Invalid Receiver Document: {document}")
        if len(document_as_digits) == 11:
            self.__document = document_as_digits
        if len(document_as_digits) == 14:
            self.__company_document = document_as_digits

    def set_address(self, address: Address) -> None:
        self.__address = address

    def get_address(self) -> Optional[Address]:
        return self.__address

    def asdict(self):
        asdict = dict(**vars(self), note="")
        del asdict[f"_{self.__class__.__name__}__address"]
        document = asdict.pop("_Sender__document")
        company_document = asdict.pop("_Sender__company_document")
        if document:
            asdict["document"] = document
        if company_document:
            asdict["company_document"] = company_document
        self.__address and asdict.update(self.__address.asdict())
        return asdict
