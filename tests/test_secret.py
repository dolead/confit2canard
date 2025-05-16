from confit2canard.secret import Secret


def test_secret():
    passkey = "Helloworld"
    secret = Secret(passkey)

    assert len(secret) == len(passkey)
    assert secret != passkey
    assert all(e == "*" for e in str(secret))
    assert secret.getSecret().decode("utf-8") == passkey
