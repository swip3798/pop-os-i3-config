import argparse

parser = argparse.ArgumentParser(description='Install i3 window manager and related software.')
parser.add_argument("--light-dm", help="Install lightdm display manager", action="store_true")
parser.add_argument("--no-restricted", help="Don't install the ubuntu-restricted extras", action="store_true")
parser.add_argument("--dev-tools", help="Install dev tools like flutter, rust toolchain and stuff", action="store_true")

import logging
import logging.handlers
from sys import stdout
logging.basicConfig(format='%(levelname)s [%(asctime)s]:%(message)s', level=logging.INFO, handlers=[
        logging.handlers.RotatingFileHandler("install.log", encoding="utf-8", maxBytes = 1024 * 16, backupCount = 5),
        logging.StreamHandler(stdout)
])
import installs

installs.i3_gaps()