import ipaddress
from collections.abc import Sequence
from typing import Self

import routeros_api
import structlog
from pydantic import BaseModel, Field

from metallb_pool_operator.env import Env


class IPv6Pool(BaseModel):
    id: str
    name: str
    prefix: str
    prefix_length: int = Field(alias="prefix-length")
    expires_after: str = Field(alias="expires-after")
    dynamic: str

    def with_postfix(self, postfix: int, cidr: int) -> Self:
        network = ipaddress.ip_network(self.prefix)
        base_addr = int(network.network_address)

        pool_base_addr = base_addr | postfix
        structured_pool_addr = ipaddress.IPv6Address(pool_base_addr)
        pool_network = ipaddress.IPv6Network((structured_pool_addr, cidr), strict=False)

        ret = self.model_copy()
        ret.prefix = str(pool_network)
        return ret


def get_ipv6_pools() -> Sequence[IPv6Pool]:
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
    return ipv6_pools


if __name__ == "__main__":
    get_ipv6_pools()
