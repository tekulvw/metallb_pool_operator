import os
from dataclasses import MISSING, dataclass, fields
from typing import ClassVar, Self


@dataclass
class Env:
    PREFIX: ClassVar = "METALLB_POOL_OP"

    ip_address: str
    username: str
    password: str
    pool_name: str
    pool_namespace: str
    port: int = 8728
    use_ssl: bool = False
    ssl_verify: bool = True
    static_addresses: str = ""

    @classmethod
    def load(cls) -> Self:
        args = {}
        for field in fields(cls):
            if field.default == MISSING:
                val = os.environ[f"{cls.PREFIX}_{field.name.upper()}"]
            else:
                val = os.environ.get(
                    f"{cls.PREFIX}_{field.name.upper()}",
                    field.default,
                )

            args[field.name] = val

        return cls(**args)
