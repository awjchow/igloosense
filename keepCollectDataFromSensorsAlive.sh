#!/bin/bash

until [  sudo python collectDataFromSensors.py ]; do
    echo "python 'collectDataFromSensors.py' crashed with exit code $?.  Respawning.." >&2
    sleep 1
done