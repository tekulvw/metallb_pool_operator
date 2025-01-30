import pytest
from metallb_pool_operator.env import Env


def test_load(monkeypatch):
    ip_address = "127.0.0.1"
    username = "testing"
    password = "notsosecret"

    monkeypatch.setenv(f"{Env.PREFIX}_IP_ADDRESS", ip_address)
    monkeypatch.setenv(f"{Env.PREFIX}_USERNAME", username)
    monkeypatch.setenv(f"{Env.PREFIX}_PASSWORD", password)

    env = Env.load()

    assert env.ip_address == ip_address
    assert env.username == username
    assert env.password == password


def test_load_missing_args():
    with pytest.raises(KeyError):
        Env.load()
