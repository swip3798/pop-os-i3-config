import os
import logging

def _(command: str) -> int:
    logging.info("Executing command: '{}'".format(command))
    return os.system(command)