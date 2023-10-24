from dataclasses import dataclass


@dataclass
class Address:
    address: str
    complement: str
    number: str
    district: str
    city: str
    postal_code: str
    state_abbr: str
    country_id: str = "BR"

    def asdict(self):
        return vars(self)
