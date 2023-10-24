from dataclasses import dataclass
from typing import Dict


@dataclass
class Config:
    use_sandbox: bool = True
    token: str = ""

    def get_base_url(self) -> str:
        return (
            self.use_sandbox
            and "https://sandbox.melhorenvio.com.br"
            or "https://melhorenvio.com.br"
        )

    def get_headers(self) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "User-Agent": "pymelhorenvio (mail@mail.com)",
        }

    def get_token(self) -> str:
        return self.token
