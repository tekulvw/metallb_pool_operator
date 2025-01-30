import os
from dataclasses import MISSING, dataclass, fields
from typing import Self


@dataclass
class Env:
    PREFIX = "METALLB_POOL_OP"
    ip_address: str
    username: str
    password: str
    port: int = 8728
    use_ssl: bool = False
    ssl_verify: bool = True

    @classmethod
    def load(cls) -> Self:
        args = {}
        for field in fields(cls):
            print(field.default)
            if field.default == MISSING:
                val = os.environ[f"{cls.PREFIX}_{field.name.upper()}"]
            else:
                val = os.environ.get(
                    f"{cls.PREFIX}_{field.name.upper()}",
                    field.default,
                )

            args[field.name] = val

        return cls(**args)
