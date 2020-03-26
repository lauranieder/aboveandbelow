# Above and Below Pollution Sensor

## UnityPackages

## aboveAndBelowUnity


## aboveAndBelowPython

The source code contained in this folder must be installed on the raspberry Pi. 

The exact path to the dataStreamer.py file must be :
```
/home/pi/aboveandbelow/aboveAndBelowPython/dataStreamer.py
```
Otherwise the script to launch the python automatically will need to be adapted. 

To test if the code is running you can simply open a terminal and type :
```
python3 /home/pi/aboveandbelow/aboveAndBelowPython/dataStreamer.py
```

It should tell you
```
connected to: /dev/ttyACM0
```
and then throw some data like
```
{"pm25": "5.00", "pm10": "8.80", "co2": "1668.00", "tvoc": "306.00", "tempC": "26.70", "tempF": "80.06", "humidityRH": "20.35", "pressurePa": "95373.99", "pressureInHg": "28.16", "altitudeM": "507.61", "altitudeF": "1665.37"}
```

### Autolaunch

Open a terminal window on the Pi and type.
```
sudo crontab -e
```
It will open the crontab file that you can edit using nano and type. 
```
@reboot bash /home/pi/aboveandbelow/aboveAndBelowPython/startupStream.sh
```
Don't forget to save. (Nano reminder : To quit, CTRL+X and then hit Y or O to save. If you are not familiar with nano text editor on Pi check a tutorial online. )

## aboveAndBelowArduino



