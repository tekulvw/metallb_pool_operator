from collections.abc import Sequence

import routeros_api
import structlog
from pydantic import BaseModel, Field

from metallb_pool_operator.env import Env


class IPv6Pool(BaseModel):
    id: str
    name: str
    prefix: str
    prefix_length: str = Field(alias="prefix-length")
    expires_after: str = Field(alias="expires-after")
    dynamic: str


def get_ipv6_pools() -> Sequence[str]:
    env = Env.load()

    pool = routeros_api.RouterOsApiPool(
        host=env.ip_address,
        username=env.username,
        password=env.password,
        port=env.port,
        use_ssl=env.use_ssl,
        ssl_verify=env.ssl_verify,
        plaintext_login=True,
    )
    api = pool.get_api()

    log = structlog.get_logger()
    ipv6_pools = [IPv6Pool(**p) for p in api.get_resource("/ipv6/pool").get()]

    log.info("got pools", **{p.name: p.prefix for p in ipv6_pools})


if __name__ == "__main__":
    get_ipv6_pools()
