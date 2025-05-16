import os
from subprocess import Popen, PIPE


SECRET_KEY = "ThisIsSupposedToBeAKey0000000000"


def test_cli_decrypt():
    configdump = Popen(
        [
            "python3",
            "-m",
            "confit2canard",
            "--key",
            SECRET_KEY,
            "--print",
            "tests/secrets/keys.yml",
        ],
        env={**dict(os.environ), "EDITOR": "cat"},
        stdout=PIPE,
        stderr=PIPE,
    )

    configdump.wait()
    assert 0 == configdump.returncode
    stdout = configdump.stdout.read().decode("utf-8").strip()
    assert "token: patriot" == stdout


def test_cli_decrypt_print():
    configdump = Popen(
        [
            "python3",
            "-m",
            "confit2canard",
            "--key",
            SECRET_KEY,
            "--print",
            "tests/secrets/keys.yml",
        ],
        env={**dict(os.environ)},
        stdout=PIPE,
        stderr=PIPE,
    )

    configdump.wait()
    assert 0 == configdump.returncode
    stdout = configdump.stdout.read().decode("utf-8").strip()
    assert "token: patriot" == stdout


def test_cli_decrypt_through_env():
    configdump = Popen(
        ["python3", "-m", "confit2canard", "--print", "tests/secrets/keys.yml"],
        env={**dict(os.environ), "VAULT_PASSKEY": SECRET_KEY},
        stdout=PIPE,
        stderr=PIPE,
    )

    configdump.wait()
    assert 0 == configdump.returncode
    stdout = configdump.stdout.read().decode("utf-8").strip()
    assert "token: patriot" == stdout


def test_cli_decrypt_bad_key():
    configdump = Popen(
        ["python3", "-m", "confit2canard", "--print", "tests/secrets/keys.yml"],
        env={**dict(os.environ), "VAULT_PASSKEY": "badkey"},
        stdout=PIPE,
        stderr=PIPE,
    )

    configdump.wait()
    assert 0 == configdump.returncode
    stdout = configdump.stdout.read().decode("utf-8").strip()
    assert "" == stdout
