#!/bin/bash
if pgrep -f dataStreamer.py >/dev/null
then
     echo "Process dataStreamer is running."
else
     echo "Process dataStreamer is not running. Starting dataStreamer.py."
   	 python3 /home/pi/aboveandbelow/aboveAndBelowPython/dataStreamer.py &
fi
