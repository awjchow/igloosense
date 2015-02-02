#!/bin/bash

sudo apt-get upgrade 	#sudo apt-get update
sudo apt-get install build-essential python-dev python-setuptools bluez pulseaudio-module-bluetooth python-bluez python-gobject python-gobject-2 bluez-tools
sudo apt-get install libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev
sudo easy_install -U distribute
sudo apt-get install python-pip
sudo pip install rpi.gpio



#cd Temperature
#sudo python setup.py install
