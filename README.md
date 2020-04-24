# Above and Below Pollution Sensor

## UnityPackages

## aboveAndBelowUnity


## aboveAndBelowArduino

### Source code
In *aboveAndBelowArduino/AB_Arduino_ReadPollutionSensors/AB_Arduino_ReadPollutionSensors.ino* you will find the code to upload on an Arduino. 

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

The exact path to the *dataStreamer.py* file must be :
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

At the beginning of the *dataStreamer.py*, you will find the credential to upload the data to Adafruit.io. If you want to use your own adafruit.io feed you can change the following and replace them by yours. You will also need to be adapted the unity accordingly. 
```
key = ""
username = ""
feed = ""
```

### Autolaunch

Open a terminal window on the Pi and type.
```
nano crontab -e
```
It will open the crontab file that you can edit using nano editor and type. 
```
*/2 * * * * bash /home/pi/aboveandbelow/aboveAndBelowPython/checkAndRestart.sh
```
Don't forget to save. (Nano reminder : To quit, CTRL+X and then hit Y or O to save. If you are not familiar with nano text editor on Pi check a tutorial online. )

The *checkAndRestart.sh* file contains a code that will check is the *dataStreamer.py* is still running, otherwise it will relaunch it. 

The crontab will launch this script every 2 minutes. 

```
#!/bin/bash
if pgrep -f dataStreamer.py >/dev/null
then
     echo "Process dataStreamer is running."
else
     echo "Process dataStreamer is not running. Starting dataStreamer.py."
   	 python3 /home/pi/aboveandbelow/aboveAndBelowPython/dataStreamer.py &
fi
```
Reference for finding a specific python code. 
https://stackoverflow.com/questions/16798111/how-to-find-kill-a-specific-python-program


### GPS Tracker Hat
The tracker hat we use is this one *Raspberry Pi GPRS/GPS Tracker HAT*
https://sixfab.com/product/raspberry-pi-gprs-gps-tracker-hat/


#### Tracker Hat Librairies
You can find the librairies on the Tracker Hat Github. I already added it in this github but in case you want to check if there is a new version, it is here. 
https://github.com/sixfab/Sixfab_RPi_Tracker_HAT

Because there is no readme on this github I mainly followed the instructions in this github instead https://github.com/sixfab/Sixfab_RPi_CellularIoT_App_Shield  which is very similar. 

Go to the folder where the library is installed (in our case I put it here /aboveandbelow/aboveAndBelowPython/TrackerHat) and do. **If you make changes to the _tracker.py_ file, you will need to redo this step.**
```
sudo python3 setup.py install
```
The enable serial_hw and I2C interfaces by following instructions below:
1. Run sudo raspi-config
2. Select 5 Interfacing Options
3. Enable P5 I2C
4. For P6 Serial
5. Disable Login shell to be accessible over serial
6. Enable Serial port hardware
7. Finish
8. Reboot
9. It's done.

#### GPS code
I adapted the code from *GNSS.py* to a new version *GNSS_readOnce.py* that will just read the data from the GPS sensor until it has registered a valid reading. 

To test this code, you can open a terminal and type 
```
python3 GNSS_readOnce.py
```
When a valid reading happens, it will be automatically saved in the text file *GPSdata.txt* which will be then read by the *dataStreamer.py*

Example of output data
```
46.517021666666665
6.643313333333333
04-23-2020T18:07:41Z
```

Reference for saving GPS data to a file
https://pythonspot.com/write-file/

#### GPS references
The sensor used by the Tracket Hat use the NMEA references.

Basically it will ouput GPS information this way. 
```
$GPRMC,183729,A,3907.356,N,12102.482,W,000.0,360.0,080301,015.5,E*6F
```
**A** in 3rd positions means the data is valid. 
**V** in 3rd positions means the data is void, so there is no satellite Data available.

If that happens, please **make sure the device is placed outside and you can see the sky**. Otherwise it won't work.

NMEA reference
https://www.gpsinformation.org/dale/nmea.htm

NMEA outputs data in a Degrees, Minutes, Seconds format so I made a conversion to Degrees decimal. 
https://www.latlong.net/degrees-minutes-seconds-to-decimal-degrees



##### Troubleshootting – GPIO error "Already in use"
GPIO error "Already in use" might be raised if you are doing some testing and restarting the program over and over again. 
Use this before restarting the code.
```
sudo killall pigpiod
```

#### Wifi access with PPP – PPPinstaller
Either you can use your own Wifi router or you can also try to use this.

Install the tracker Hat by following these instructions. 
https://sixfab.com/ppp-installer-for-sixfab-shield/
```
sudo ./install.sh
```
* Select number 5 / Tracker Hat. 
* For the Sim card I purchased from digitec IOT, set the APN to "dr.m2m.ch". With no credentials needed. If you are using a SIM card from a UK operator, please refer to your operator to know the APN carrier. 

The installation did not work with my swiss SIM card and with the PI 4. But in case you want to retry with another SIM feel free to. 



