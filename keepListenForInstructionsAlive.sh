#!/bin/bash

until [  python listenForInstructions.py ]; do
    echo "python 'listenForInstructions.py' crashed with exit code $?.  Respawning.." >&2
    sleep 1
done