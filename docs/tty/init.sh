#!/bin/bash

sudo apt update

sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

sudo apt install -y git nodejs npm python3-pip curl

sudo npm install -g ttystudio

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update

sudo apt-get install -y docker-ce docker-ce-cli containerd.io

sudo usermod -aG docker $USER

echo "PS1='$ '" >> ~/.bashrc
echo 'PATH=$PATH:/home/vagrant/.local/bin/' >> ~/.bashrc

git clone git@github.com:tadeugr/dugaire.git
