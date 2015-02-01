#!/bin/bash

sudo apt-get upgrade
sudo apt-get install build-essential python-dev python-setuptools bluez pulseaudio-module-bluetooth python-gobject python-gobject-2 bluez-tools
sudo easy_install -U distribute
sudo apt-get install python-pip
sudo pip install rpi.gpio
#cd Temperature
#sudo python setup.py install
