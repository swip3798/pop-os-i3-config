import logging
from base import _, apt_install, apt_update, apt_upgrade
from constants import BASIC_SOFTWARE, LIGHTDM_SOFTWARE
import os
import subprocess
import re
import datetime

I3_GITURL = "https://github.com/Airblader/i3.git"
I3_BRANCH_NEXT = "gaps-next"
I3_BRANCH_DEFAULT = "gaps"
I3_GITDIR="i3-gaps"
I3_PATCHDIR="patches"

def basics():
    # Add 32bit architecture for later use of wine and steam
    _("sudo dpkg --add-architecture i386")

    # Update and Upgrade
    apt_update()
    apt_upgrade()

    # Base install
    apt_install(BASIC_SOFTWARE)

    # Set askpass
    _('echo "Path askpass /usr/bin/ssh-askpass" | sudo tee /etc/sudo.conf')

    # Copy desktop files
    _("cp ./desktop-files/*.desktop ~/.local/share/applications/")

def restricted_extras():
    apt_install(["ubuntu-restricted-extras"])

def light_dm():
    apt_install(LIGHTDM_SOFTWARE)

def copy_configs():
    _("mkdir ~/.config")
    _("cp -r ./config/* ~/.config/")

def build_startup_script(arandr_layout: bool, conky: bool, nitrogen: bool = True):
    startups = []
    startups.append("nitrogen --restore")
    startups.append("bash ~/.screenlayout/default.sh")
    

def i3_gaps(install_next: bool = True):
    logging.info("Install dependencies")
    _("sudo apt -y build-dep i3-wm")
    apt_install([
        "devscripts",
        "dpkg-dev",
        "dh-autoreconf",
        "libxcb-xrm-dev",
        "libxcb-xkb-dev", 
        "libxkbcommon-dev", 
        "libxkbcommon-x11-dev",
        "libxcb-shape0-dev",
        "meson",
    ])

    logging.info("Clone repository")
    _("git clone {} {}".format(I3_GITURL, I3_GITDIR))
    os.chdir(I3_GITDIR)

    logging.info("Cleanup repository")
    _("git reset --hard HEAD")
    _("git clean -fdx")
    branch = I3_BRANCH_DEFAULT
    if install_next:
        branch = I3_BRANCH_NEXT

    logging.info("Change to correct branch")
    _("git checkout {}".format(branch))
    _("git pull --no-rebase")

    logging.info("Build i3-gaps")
    debian_version = subprocess.check_output(["head", "-1", "debian/changelog"]).decode("utf-8")    
    regex = r"\((.+)\-"
    debian_version = re.findall(regex, debian_version)[0]
    i3version = ""
    with open("I3_VERSION", "r") as f:
        i3version = f.read().split("-")[0]
    res = _("dpkg --compare-versions {} lt {}".format(debian_version, i3version))
    version = debian_version
    if res == 0:
        version = i3version
    dt = datetime.datetime.now()
    timestamp = dt.strftime("%Y%m%d%H%M%S")
    newVersion = "{}-1gerado+{}".format(version, timestamp)
    os.environ["DEBEMAIL"] = "annialisisch@gmail.com"
    os.environ["DEBFULLNAME"] = "Christian S."
    _('debchange --dist=unstable --newversion="{}" "New upstream."'.format(newVersion))
    _('patch --forward -r - -p1 <{}/0001-debian-Disable-sanitizers.patch'.format(I3_PATCHDIR))
    with open("debian/rules", "a") as f:
        f.write("override_dh_install:\n")
        f.write("override_dh_installdocs:\n")
        f.write("override_dh_installman:\n")
        f.write("\tdh_install -O--parallel\n")
    _("dpkg-buildpackage -us -uc")
    os.chdir("..")
    _("sudo dpkg -i i3_*{0}*deb i3-wm_*{0}*deb".format(timestamp))
    _("rm -v *{}*".format(timestamp))
        

def dev_tools():
    _("bash dev-tools-install.sh")

def sec_tools():
    _("bash sec-stuff.sh")