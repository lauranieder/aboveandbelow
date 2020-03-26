#!/bin/bash

while true
do
	printf "RELAUNCH"
	python3 /home/pi/aboveandbelow/aboveAndBelowPython/dataStreamer.py &
	sleep 120
	printf "KILL PYTHON"
	pkill -9 python
	sleep 5
done
