import math

from subprocess import *
from random import randrange

import BMP085 as BMP085

import class_gps as gpsreader


# Setup encironment sensor
environment_sensor = BMP085.BMP085()

# Start GPS Poller
gps_poller = gpsreader.gpsPoller()
gps_poller.start()


## Get data from vehicle components
def getBatteryA():
    return(randrange(100))

def getBatteryB():
    return(randrange(100))

def getWifi():
    getwifidata_cmd = "awk 'NR==3 {print $3}' /proc/net/wireless | cut -c 1-2"
    wifi_value = _run_cmd(getwifidata_cmd)

    try:
        wifi_value = int(wifi_value)
        return(wifi_value)

    except:
        return(0)


## Get environment data
def getEnvironment_temperature():
    temperature = environment_sensor.read_temperature()
    return(temperature)

def getEnvironment_humidity():
    return(randrange(100))

def getEnvironment_pressure():
    pressure = environment_sensor.read_pressure()
    return(pressure)



## Get GPS data
def getGPS_lat():
    if gps_poller.gpsdata['status'] == "FIX":
        return gps_poller.gpsdata['latitude']
    else:
        return(gps_poller.gpsdata['status'])

def getGPS_long():
    if gps_poller.gpsdata['status'] == "FIX":
        return gps_poller.gpsdata['longitude']
    else:
        return(gps_poller.gpsdata['status'])

def getGPS_speed():
    if gps_poller.gpsdata['status'] == "FIX":
        return math.floor(gps_poller.gpsdata['speed'])
    else:
        return(gps_poller.gpsdata['status'])

def getGPS_altitude():
    if gps_poller.gpsdata['status'] == "FIX":
        return gps_poller.gpsdata['altitude']
    else:
        return(gps_poller.gpsdata['status'])


## Run external commands, returns output
def _run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output
