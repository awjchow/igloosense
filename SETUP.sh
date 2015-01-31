#!/bin/bash

sudo apt-get upgrade
sudo apt-get install build-essential python-dev python-setuptools
sudo easy_install -U distribute
sudo apt-get install python-pip
sudo pip install rpi.gpio
cd Temperature
sudo python setup.py install