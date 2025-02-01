import pytest

from metallb_pool_operator.env import Env


def test_load(monkeypatch):
    ip_address = "127.0.0.1"
    username = "testing"
    password = "notsosecret"  # noqa: S105
    pool_name = "pool"
    pool_namespace = "space"

    monkeypatch.setenv(f"{Env.PREFIX}_IP_ADDRESS", ip_address)
    monkeypatch.setenv(f"{Env.PREFIX}_USERNAME", username)
    monkeypatch.setenv(f"{Env.PREFIX}_PASSWORD", password)
    monkeypatch.setenv(f"{Env.PREFIX}_POOL_NAME", pool_name)
    monkeypatch.setenv(f"{Env.PREFIX}_POOL_NAMESPACE", pool_namespace)

    env = Env.load()

    assert env.ip_address == ip_address
    assert env.username == username
    assert env.password == password
    assert env.pool_name == pool_name
    assert env.pool_namespace == pool_namespace


def test_load_missing_args():
    with pytest.raises(KeyError):
        Env.load()
