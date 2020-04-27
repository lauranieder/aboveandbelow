#!/bin/bash
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

print("Arduino connected to: " + ser.portstr)

#this will store the line
seq = []
count = 1
started = 0
joined_seq = "";
lines = []
data = []
dataToSend = []

#ReadGPSData from a file
path = "/home/pi/aboveandbelow/aboveAndBelowPython/TrackerHat/"
filename = "GPSdata.txt"

def readGPSData(file):
    myfile = open(file, 'r')
    lines =myfile.readlines()
    i = 0
    if len(lines) == 3:
        for x in lines:
            if i == 0:
                try:
                    float(x)
                    lat = x.strip()
                except ValueError:
                    return ["0", "0", "Formatting error in the GPSdata. Lat is not a float."]
            elif i == 1:
                try:
                    float(x)
                    long = x.strip()
                except ValueError:
                    return ["0", "0", "Formatting error in the GPSdata. Long is not a float."]
            elif i == 2:
                date_time = x.strip()
            i = i+1
        return [str(float(lat)), str(float(long)), str(date_time)]
    else:
        return ["0", "0", "Formatting error in the GPSdata. Line number incorrect."]



while True:
    for c in ser.read():
        if chr(c) == '&':
            started = 1
            data = []
            dataToSend = []
        if started == 1:
            seq.append(chr(c)) #convert from ANSII
        if chr(c) == '#':#\n
            joined_seq = ''.join(seq)
            lines = joined_seq.split(',')
            inc = 0
            for v in lines:
                if inc > 0:
                    temp = v.split('=')
                    if len(temp) == 2:
                        data.append(temp[1])
                inc += 1
                temp = []
            if len(data) > 10:
                GPSdata = readGPSData(path+filename)
                sensorData = {
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
                    "lat":GPSdata[0],
                    "lon":GPSdata[1],
                    "gdat":GPSdata[2],
                }
                sensorDataDumped = json.dumps(sensorData)

                localisationData = {
                    "lat":"4",
                    "lon":"5",
                    "gdat":"hellworld",
                }
                localisationDataDumped = json.dumps(localisationData)

                dataToSend = {
                    "value": sensorDataDumped,
                    "gps":localisationDataDumped,
                }
                #print(str(GPSdata[2]))
                with requests.Session() as s:
                    r = s.post(url, json = dataToSend, headers = headers)
                    print(r.status_code, flush=True)
                    print(r.text, flush=True)
                seq = []
                count += 1
                joined_seq = "";
                started = 0
                break


ser.close()
