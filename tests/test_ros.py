import pytest

from metallb_pool_operator.ros import IPv6Pool


@pytest.fixture
def pool():
    return IPv6Pool(
        **{
            "id": "0",
            "name": "dhcp-pool",
            "prefix": "2600:6c82:f00:127::/64",
            "prefix-length": "72",
            "expires-after": "never",
            "dynamic": "yes",
        },
    )


def test_with_postfix(pool: IPv6Pool):
    new_pool = pool.with_postfix(0x3000, 116)

    assert new_pool.prefix_length == pool.prefix_length
    assert new_pool.prefix == "2600:6c82:f00:127::3000/116"
