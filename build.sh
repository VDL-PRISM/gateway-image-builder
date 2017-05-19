#!/bin/bash -e
set -x

# Set default locales to 'en_US.UTF-8'
echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen
locale-gen

# Install Docker
curl -sSL get.docker.com | sh

# Set up docker to work on non-root users

# Install basic software
apt-get install -y zip unzip avahi-daemon git python-yaml

# Install ngrok
curl -O https://bin.equinox.io/c/gDfFGFRN2Jh/ngrok-link-stable-linux-arm.tgz
tar -xvzf ngrok-link-stable-linux-arm.tgz
mv ngrok /usr/local/bin
rm ngrok-link-stable-linux-arm.tgz

# Cleanup
apt-get clean
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
