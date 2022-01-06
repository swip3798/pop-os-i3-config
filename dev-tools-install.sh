# This just installs the basic tools i need for most development tasks for my private software development
mkdir -p ~/Documents/dev

####### VSCODE #########
mkdir vscode
cd vscode
wget "https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64" -O vscode.deb
sudo dpkg -i vscode.deb
rm -f vscode.deb
cd ..

######## RUST ##########
# install rust toolchain
# Redundant because already installed for building alacritty
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

###### PYTHON ###########
sudo apt install -y python3-pip
pip install seaborn pandas mongoengine scikit-learn requests sqlalchemy tornado flask


####### FLUTTER #########
# Install flutter (except android studio stuff, because of the pain) works for 2.8.1
sudo snap install flutter --classic

flutter config --no-analytics
flutter doctor

# Linux desktop dependencies
sudo apt-get install -y clang cmake ninja-build pkg-config libgtk-3-dev
# Enable desktop support
flutter config --enable-linux-desktop

# Android Studio 
sudo snap install android-studio --classic
echo Now android studio gets opened, install android studio and install command-line tools
android-studio
echo Press enter when you installed both android studio and command-line tools
read -p " [RETURN]"
flutter doctor --android-licenses
flutter doctor

####### Install Docker #########
sudo apt install -y ca-certificates gnupg lsb-releases

curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

sudo docker run hello-world

####### Github CLI #########
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
gh auth login