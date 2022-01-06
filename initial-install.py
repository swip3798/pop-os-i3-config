import os
import argparse

from base import _
import installs

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

args = parser.parse_args()
#print(args)

# Add 32bit architecture for later use of wine and steam
_("sudo dpkg --add-architecture i386")

# Update and Upgrade
_("sudo apt update")
_("sudo apt upgrade -y")

# Base install
_("sudo apt install -y i3 lxappearance nitrogen pulseaudio pavucontrol alsa-utils unzip arc-theme compton rofi neofetch arandr snapd curl ssh-askpass-fullscreen alacritty")

if not args.no_restricted:
    _("sudo apt install -y ubuntu-restricted-extras")
else:
    logging.info("ubuntu-restricted-extras skipped")

# Lightdm install
if args.light_dm:
    _("sudo apt install -y lightdm lightdm-settings slick-greeter")
else:
    logging.info("No Lightdm installation")

# Set askpass
_('echo "Path askpass /usr/bin/ssh-askpass" | sudo tee /etc/sudo.conf')

# Copy desktop files
_("cp ./desktop-files/*.desktop ~/.local/share/applications/")

# Build and install i3-gaps
installs.i3_gaps()

# Copy configs
_("mkdir ~/.config")
_("cp -r ./config/* ~/.config/")

if args.dev_tools:
    installs.dev_tools()