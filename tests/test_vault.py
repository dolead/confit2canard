import json
import pytest

from confit2canard import Vault, Secret

SECRET_KEY = "ThisIsSupposedToBeAKey0000000000".encode("utf-8")
PAYLOAD = {"Water": "wet", "Fire": "burns"}
ENCRYPTED_PAYLOAD = (
    "$Vault;mp4C9+rlUYCRttbL;7fs4rsL2KrC3MZ1g2a8GFn"
    "Nvoki35cZyi4HI2ggmnHo1;sPQ2X70aDhHXXWh4xOi3Hw=="
)


def test_encrypt_vault():
    vault = Vault(SECRET_KEY)
    encrypted = vault.encrypt(json.dumps(PAYLOAD))
    assert encrypted.startswith(vault.prefix())


def test_encrypt_vault_from_secret():
    secret = Secret(SECRET_KEY)
    vault = Vault(secret)
    encrypted = vault.encrypt(json.dumps(PAYLOAD))
    assert encrypted.startswith(vault.prefix())


def test_encrypt_vault_from_secret_exception():
    vault = Vault(SECRET_KEY)
    with pytest.raises(RuntimeError):
        vault.decrypt(
            ";;7fs4rsL2KrC3MZ1g2a8GFnNvoki35cZyi4HI2ggmnHo1;sPQ2X70aDhHXXWh4xOi3Hw=="
        )
    with pytest.raises(ValueError):
        vault.decrypt(
            "7fs4rsL2KrC3MZ1g2a8GFnNvoki35cZyi4HI2ggmnHo1;sPQ2X70aDhHXXWh4xOi3Hw=="
        )


def test_decrypt_vault():
    vault = Vault(SECRET_KEY)
    cleartext = vault.decrypt(ENCRYPTED_PAYLOAD)
    assert not cleartext.startswith(vault.prefix())
    payload = json.loads(cleartext)
    for key, value in PAYLOAD.items():
        assert key in payload
        assert payload.get(key) == value
