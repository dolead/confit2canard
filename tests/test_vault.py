import json

from confit2canard import Vault

SECRET_KEY="ThisIsSupposedToBeAKey0000000000".encode("utf-8")  # noqa
PAYLOAD={"Water": "wet", "Fire": "burns"}
ENCRYPTED_PAYLOAD=("$Vault;mp4C9+rlUYCRttbL;7fs4rsL2KrC3MZ1g2a8GFn"
                   "Nvoki35cZyi4HI2ggmnHo1;sPQ2X70aDhHXXWh4xOi3Hw==")


def test_encrypt_vault():
    vault = Vault(SECRET_KEY)
    encrypted = vault.encrypt(json.dumps(PAYLOAD))
    assert encrypted.startswith(vault.prefix())


def test_decrypt_vault():
    vault = Vault(SECRET_KEY)
    cleartext = vault.decrypt(ENCRYPTED_PAYLOAD)
    assert not cleartext.startswith(vault.prefix())
    payload = json.loads(cleartext)
    for key, value in PAYLOAD.items():
        assert key in payload
        assert payload.get(key) == value
