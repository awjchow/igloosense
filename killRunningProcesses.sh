#!/bin/bash

PIDFile="/home/pi/Desktop/igloosense/collect.pid"
sudo kill -9 $(<"$PIDFile")
PIDFile="/home/pi/Desktop/igloosense/listen.pid"
sudo kill -9 $(<"$PIDFile")