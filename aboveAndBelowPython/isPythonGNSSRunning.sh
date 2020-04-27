#!/bin/bash
if pgrep -f GNSS_readOnce.py >/dev/null
then
     echo "Process GNSS_readOnce.py is running."
else
     echo "Process GNSS_readOnce.py is not running."
fi
