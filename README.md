# Above and Below Pollution Sensor

## UnityPackages

## aboveAndBelowUnity


## aboveAndBelowArduino

### Source code
In aboveAndBelowArduino/AB_Arduino_ReadPollutionSensors/AB_Arduino_ReadPollutionSensors.ino you will find the code to upload on an Arduino. 

Tested with 1.8.12 version of Arduino IDE.

The code relies on external librairies such as 
* [SparkFun_CCS811_Arduino_Library](https://github.com/sparkfun/SparkFun_CCS811_Arduino_Library)
* [SparkFun_BME280_Arduino_Library](https://github.com/sparkfun/SparkFun_BME280_Arduino_Library)
* [Custom made arduino library for the novaPM sensor](https://github.com/lauraperrenoud/novaPM)
 

### Wiring
Using an Arduino Uno plugged to the Raspberry Pi

#### Sparkfun environmental combo CCS811 / BME280

SDA > A4

SCL > A5

3.3V > Arduino 3.3.V

GND > Arduino Ground

#### novaPM sensor SDS011

RXD > 3

TXD > 2

5V > Arduino 5V

GND > Arduino Ground

## aboveAndBelowPython
 
I used a Raspberry Pi 4 Model B installed with Raspbian Buster. 
The OS can be found here if you need to install other Pis, I recommend using NOOBS. https://www.raspberrypi.org/downloads/raspbian/

### Installing and testing the code
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
The code runs with Python3. 

### Data stream

At the beginning of the dataStreamer.py, you will find the credential to upload the data to Adafruit.io. If you want to use your own adafruit.io feed you can change the following and replace them by yours. You will also need to adapt the unity accordingly. 
```
key = ""
username = ""
feed = ""
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

The startupStream.sh file contains a code that will run in a loop, quit and relaunch periodically the python code so if anything goes wrong, it will restart.

```
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
```
