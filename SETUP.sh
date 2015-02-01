#!/bin/bash

sudo apt-get upgrade
sudo apt-get install build-essential python-dev python-setuptools bluez pulseaudio-module-bluetooth python-bluez python-gobject python-gobject-2 bluez-tools
sudo apt-get install libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev
sudo easy_install -U distribute
sudo apt-get install python-pip
sudo pip install rpi.gpio

wget https://www.kernel.org/pub/linux/bluetooth/bluez-5.27.tar.gz
tar -xzvf bluez-5.27.tar.gz
cd ../bluez-5.27
./configure --prefix=/usr --sysconfdir=/etc  --localstatedir=/var --enable-experimental --enable-maintainer-mode --enable-library --disable-systemd
make
make check
sudo make install
#cd Temperature
#sudo python setup.py install
