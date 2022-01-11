import installs

import logging
import logging.handlers

import base as bs
from sys import stdout
logging.basicConfig(format='%(levelname)s [%(asctime)s]:%(message)s', level=logging.INFO, handlers=[
        logging.handlers.RotatingFileHandler("install.log", encoding="utf-8", maxBytes = 1024 * 16, backupCount = 5),
        logging.StreamHandler(stdout)
])

bs.prompt("This install script guides you through the i3 installation and configuration. First the basic software needs to be installed.")
installs.basics()

if bs.choice("Do you want to install the non open-source ubuntu-restricted-extras for fonts and media codecs?"):
    installs.restricted_extras()
else:
    logging.info("ubuntu-restricted-extras skipped")

# Lightdm install
if bs.choice("Do you want to install lightdm with slick greeter as your display manager? You will be prompted to select your new display manager during the installation."):
    installs.light_dm()
else:
    logging.info("No Lightdm installation")

# Build and install i3-gaps
installs.i3_gaps()

# Copy configs
installs.copy_configs()

if bs.choice("Do you want to install the dev tools? Those are only if you develop with those specific technologies."):
    installs.dev_tools()