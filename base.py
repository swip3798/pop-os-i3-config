import os
import logging


def _(command: str) -> int:
    logging.info("Executing command: '{}'".format(command))
    return os.system(command)

def apt_install(software) -> int:
    return _("sudo apt install -y {}".format(" ".join(software)))

def apt_update() -> int:
    return _("sudo apt update")

def apt_upgrade() -> int:
    return _("sudo apt upgrade -y")

