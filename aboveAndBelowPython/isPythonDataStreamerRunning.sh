#!/bin/bash
if pgrep -f dataStreamer.py >/dev/null
then
     echo "Process dataStreamer is running."
else
     echo "Process dataStreamer is not running."
fi
