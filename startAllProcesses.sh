#!/bin/bash

nohup ./keepCollectDataFromSensorsAlive.sh > /dev/null 2>&1 & echo $! > collect.pid
nohup ./keepListenForInstructionsAlive.sh > /dev/null 2>&1 & echo $! > listen.pid