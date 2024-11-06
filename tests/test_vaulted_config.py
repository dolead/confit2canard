from confit2canard.config import Config

SECRET_KEY="ThisIsSupposedToBeAKey0000000000".encode("utf-8")


def test_load_config():
    config = Config(["tests/secrets/keys.yml"])
    assert config is not None


def test_load_override_config():
    config = Config(["tests/secrets/keys.yml"])
    assert config is not None

    assert config.load("tests/clear/keys.yml")
