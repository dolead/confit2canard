from os import environ
import pytest

from confit2canard.config import Config

SECRET_KEY="ThisIsSupposedToBeAKey0000000000"  # noqa


def test_load_vaulted_config():
    with pytest.raises(RuntimeError):
        config = Config(["tests/secrets/keys.yml"])

    config = Config(["tests/secrets/keys.yml"], passkey=SECRET_KEY)
    assert config._configuration != {}
    assert config.token == "patriot"  # noqa


def test_load_envpasskey_vaulted_config():
    with pytest.raises(RuntimeError) as ex_info:
        config = Config(["tests/secrets/keys.yml"])

    assert ex_info
    environ["VAULT_PASSKEY"] = SECRET_KEY
    config = Config(["tests/secrets/keys.yml"], passkey=SECRET_KEY)
    assert config._configuration
    assert config.token == "patriot"  # noqa


def test_load_override_vaulted_config():
    config = Config(["tests/secrets/keys.yml"], passkey=SECRET_KEY)
    assert config is not None

    assert config.load("tests/clear/keys.yml")
