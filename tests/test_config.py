import pytest
from confit2canard import Config


def test_load_config():
    config = Config(["tests/clear/logging.yml"])

    assert "path" in config.find("logging")
    assert config.find("logging.level") == "INFO"
    assert config.logging.level == "INFO"
    assert isinstance(config.logging.maxsize, int)
    assert config.logging.maxsize == 1024
    assert config.surname is None
    assert config.firstname is None
    config.load("tests/clear/robin.json")
    assert config.surname == "Todd"
    assert config.firstname == "Jason"


def test_exception_on_load():
    with pytest.raises(FileNotFoundError) as ex_info:
        Config(["logging.yml"])
    assert ex_info.typename == "FileNotFoundError"


def test_ignore_missing_on_load():
    config = Config()
    config.load("logging.yml", silent=True)

    assert config.logging is None
    assert config.find("setting.that.doesnt.exist") is None


def test_override_config():
    config = Config(["tests/clear/logging.yml"])
    assert config.logging.maxsize == 1024
    assert config.logging.level == "INFO"
    config.load("tests/clear/overrides.yml")
    assert config.logging.maxsize == 2048
    assert config.logging.level == "INFO"
