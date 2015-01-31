#!/bin/bash

sudo apt-get upgrade
sudo apt-get install build-essential python-dev
cd Temperature
sudo python setup.py install
