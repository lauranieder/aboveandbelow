#!/bin/bash
if pgrep -f GNSS_readOnce.py >/dev/null
then
     echo "Process GNSS_readOnce.py is running."
else
     echo "Process GNSS_readOnce.py is not running. Starting GNSS_readOnce.py."
   	 python3 /home/pi/aboveandbelow/aboveAndBelowPython/TrackerHat/GNSS_readOnce.py &
fi
