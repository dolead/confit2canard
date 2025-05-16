#!/usr/bin/python3
import logging
import tempfile
from argparse import ArgumentParser
from os import environ, path, unlink
from subprocess import Popen
from sys import stderr
from typing import Optional

from confit2canard import Vault, Secret

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stderr)
logger.addHandler(handler)


def read_configuration(vault: Vault, configuration):
    if path.exists(configuration):
        logger.info("Reading configuration from %s", configuration)
        with open(configuration, "r") as fd:
            buffer = fd.read()
            if buffer:
                try:
                    return vault.decrypt(buffer)
                except ValueError:
                    logger.error("Couldn't decrypt, the key might not "
                                 "be valid.")


def main(configuration, passkey: Optional[Secret] = None, dump: bool = False):
    if not path.exists(path.abspath(path.dirname(configuration))):
        logger.error("Parent folder for %s doesn't exist", configuration)
        return
    if passkey is None:
        env_passkey = environ.get("VAULT_PASSKEY")
        if not env_passkey:
            logging.error("Passkey is missing")
            return
        passkey = Secret(env_passkey)
    vault = Vault(passkey)
    editor = environ.get("EDITOR")
    if not editor:
        logging.error("EDITOR environment variable not set")
        return

    extension = "." + configuration.split(".")[-1]
    old = ""
    if dump:
        print(read_configuration(vault, configuration) or "")
        return

    with tempfile.NamedTemporaryFile(delete=False, suffix=extension,
                                     mode="w") as tfile:
        old = read_configuration(vault, configuration)
        if not old:
            tfile.close()
            unlink(tfile.name)
        process = Popen([editor, tfile.name])
        process.wait()

        if process.returncode != 0:
            logging.error("An error occurred with editor %s", editor)
            return

        with open(tfile.name, "r") as fd:
            payload = fd.read()

    if len(payload) == 0:
        logger.info("Nothing to write")
        return
    if payload != "":
        payload = vault.encrypt(payload)
    try:
        with open(configuration, "w+") as fd:
            fd.write(payload)
            logger.info("Writing %d bytes", len(payload))
    except PermissionError:
        logger.error("Couldn't write configuration to file: %s", payload)


if __name__ == "__main__":
    args = ArgumentParser("Confit2Canard")
    args.add_argument("config", action="store",
                      help="The path to the file to edit")
    args.add_argument("--key", action="store",
                      help="Passkey to decrypt and encrypt",
                      type=lambda s: Secret(s.encode("utf-8")))
    args.add_argument("--print", action="store_true",
                      help="Print payload to STDOUT")
    parsed = args.parse_args()
    main(parsed.config, parsed.key, parsed.print)
