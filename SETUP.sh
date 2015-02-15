#!/bin/bash

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-dev
sudo apt-get install python-rpi.gpio #(the RPi to Python bridge)
sudo apt-get install python-setuptools
sudo easy_install pip
sudo pip install boto



sudo apt-get install build-essential bluez python-bluez python-gobject python-gobject-2 bluez-tools
sudo apt-get install libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev
sudo easy_install -U distribute
sudo apt-get install python-pip
sudo pip install rpi.gpio

sudo apt-get install nodejs npm node-semver		#to install npm to get pm2

#cd Temperature
#sudo python setup.py install


