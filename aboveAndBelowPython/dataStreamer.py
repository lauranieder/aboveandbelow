import serial
import time
import json
import random
import requests
import sys

key = "0986d2e6e2414ace88d8c82d8aad0316"
username = "fragmentin"
feed = "ab-pollution"
#
url = "https://io.adafruit.com/api/v2/"+username+"/feeds/"+feed+"/data"
headers = {
    "Content-Type": "application/json",
    "X-AIO-Key": key,
}

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0
)

print("connected to: " + ser.portstr)

#this will store the line
seq = []
count = 1
started = 0
joined_seq = "";
lines = []
data = []


while True:
    for c in ser.read():
        if chr(c) == '&':
            started = 1
            data = []
        if started == 1:
            seq.append(chr(c)) #convert from ANSII
##         joined_seq = ''.join(str(v) for v in seq) #Make a string from array
        if chr(c) == '#':#\n
            joined_seq = ''.join(seq)
            ##print(joined_seq)
            lines = joined_seq.split(',')
##            print("line : ")
            inc = 0
            for v in lines:
                if inc > 0:
                    temp = v.split('=')
                    ##for t in temp:
                        ##print(t)
                    if len(temp) == 2:
                        data.append(temp[1])
                        ##print("line to append : "+temp[1])

##                else:
                inc += 1
                temp = []

            #print(v)
            if len(data) > 10:
                fakeJson = {
                    "pm25": data[0],
                    "pm10": data[1],
                    "co2": data[2],
                    "tvoc": data[3],
                    "tempC": data[4],
                    "tempF": data[5],
                    "humidityRH": data[6],
                    "pressurePa": data[7],
                    "pressureInHg": data[8],
                    "altitudeM": data[9],
                    "altitudeF": data[10],
                }
                dumped = json.dumps(fakeJson)
                #print("ddd: "+dumped)
                data = {
                    "value": dumped,
                    "lat":random.random(),
                    "lon":random.random(),
                }
                #dumped = json.dumps(data)
                #print(data)
                with requests.Session() as s:
                    r = s.post(url, json = data, headers = headers)
                    print(r.status_code, flush=True)
                    print(r.text, flush=True)
                seq = []
                count += 1
                joined_seq = "";
                started = 0
                break


ser.close()
