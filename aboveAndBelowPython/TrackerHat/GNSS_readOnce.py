'''
  basicUDP.py - This is basic UDP example.
  Created by Yasin Kaya (selengalp), January 2, 2019.
  Modified by Saeed Johar (saeedjohar), October 3, 2019.
'''
# import sys
from tracker import tracker
from time import sleep
from datetime import datetime


# log = open("/home/pi/aboveandbelow/aboveAndBelowPython/TrackerHat/GNSS-log.log","a")
# sys.stdout = log
# print = log.info

node = tracker.Tracker()

node.Sendline()
node.readNMEA()
sleep(2)

foundGPSdata = 0



def isValid(data):
    if len(data) < 14:
        print("Incorrect data format. Line incomplete "+str(len(data)))
        logLine("Incorrect data format. Line incomplete "+str(len(data)))
        return 0
    if data[0:6] == "$GPRMC" or data[0:6] == "$GNRMC":
        sdata = data.split(",")
        if sdata[2] == 'V':
            print ("No satellite data available.")
            logLine("No satellite data available.")
            return 1
        print ("-----Parsing GPRMC/GNRMC-----")
#         logLine("-----Parsing GPRMC/GNRMC-----")
        time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
        lat = decodeDecimal(sdata[3]) #latitude
        dirLat = sdata[4]      #latitude direction N/S
        lon = decodeDecimal(sdata[5]) #longitute
        dirLon = sdata[6]      #longitude direction E/W
        speed = sdata[7]       #Speed in knots
        trCourse = sdata[8]    #True course
        date = sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6]
        variation = sdata[10]  #variation
        degreeChecksum = sdata[11]
        print ("time : %s, latitude : %s(%s), longitude : %s(%s), speed : %s, True Course : %s, Date : %s, Magnetic Variation : %s,Checksum : %s "%    (time,lat,dirLat,lon,dirLon,speed,trCourse,date,variation, degreeChecksum))
        logLine("Data : latitude : "+lat+"  longitude : "+lon)
        save(lat,lon)
        return 1
    else:
        print ("No GPS Data. Parsed data is ",data[0:6])
        logLine("No GPS Data. Parsed data is "+str(data[0:6]))
        return 0

def parseGPS(data):
    print ("______")
    print ("raw:", data) #prints raw data
    print ("______")
    dataByLine = data.splitlines()
    #print (" Data Lines: "+str(len(dataByLine)));
    for l in dataByLine:
        #print(str(isValid(l)))
        foundGPDdata = (isValid(l))
        if foundGPDdata == 1:
            return
    
def decode(coord):
    #Converts DDDMM.MMMMM -> DD deg MM.MMMMM min
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"

def decodeDecimal(coord):
    #Converts DDDMM.MMMMM -> DD.DDDDDDD with decimal
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    degf = head[0:-2]
    minf = head[-2:]
    #print(degf)
    fullminf = minf+"." + tail
    min = float(fullminf)/60
    deg = float(degf)
    deg = deg + min
    return str(deg)


def save(lat, long):
    # current date and time
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    #Converts DDDMM.MMMMM -> DD deg MM.MMMMM min
    # Filename to write
    path = "/home/pi/aboveandbelow/aboveAndBelowPython/TrackerHat/"
    filename = "GPSdata.txt"
    # Open the file with writing permission
    myfile = open(path+filename, 'w')
    # Write a line to the file
    myfile.write(lat+'\n'+long+'\n'+str(date_time)+'\n')
    # Close the file
    myfile.close()
    foundGPSdata = 1
    
def logLine(lineToLog):
    # current date and time
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    #Converts DDDMM.MMMMM -> DD deg MM.MMMMM min
    # Filename to write
    path = "/home/pi/aboveandbelow/aboveAndBelowPython/TrackerHat/"
    filename = "GNSSLog.log"
    # Open the file with writing permission
    myfile = open(path+filename, 'a')
    # Write a line to the file
    myfile.write("["+str(date_time)+"]  "+str(lineToLog)+'\n')
    # Close the file
    myfile.close()
    

while foundGPSdata == 0:
    
    message = node.readNMEA()
    msg = message.decode(encoding="utf-8", errors='ignore')
    #print(msg)
    parseGPS(msg)
    msg = ""
    sleep(3)
