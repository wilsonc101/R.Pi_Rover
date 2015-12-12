import math
from random import randrange
from subprocess import *

import Adafruit_BMP085 as BMP085
import Adafruit_LSM303 as LSM303


# Setup environment sensor
ENV_SENSOR = BMP085.BMP085()

# vehicle movement sensor
MOVE_SENSOR = LSM303.Adafruit_LSM303(hires="false")

## Get data from vehicle components
def getBatteryA():
    return randrange(100)

def getBatteryB():
    return randrange(100)

def getWifi():
    getwifidata_cmd = "awk 'NR==3 {print $4}' /proc/net/wireless | cut -c 1-3"
    wifi_value = _run_cmd(getwifidata_cmd)

    try:
        wifi_value = 100 + int(wifi_value)
        return wifi_value

    except:
        return 0


## Get environment data
def getEnvironment_temperature():
    temperature = ENV_SENSOR.readTemperature()
    return temperature

def getEnvironment_humidity():
    return randrange(100)

def getEnvironment_pressure():
    pressure = ENV_SENSOR.readPressure()
    return pressure



## Get GPS data
def getGPS_lat(gps_poller):
    if gps_poller.gpsdata['status'] == "FIX":
        return gps_poller.gpsdata['latitude']
    else:
        return gps_poller.gpsdata['status']

def getGPS_long(gps_poller):
    if gps_poller.gpsdata['status'] == "FIX":
        return gps_poller.gpsdata['longitude']
    else:
        return gps_poller.gpsdata['status']

def getGPS_speed(gps_poller):
    if gps_poller.gpsdata['status'] == "FIX":
        return math.floor(gps_poller.gpsdata['speed'])
    else:
        return gps_poller.gpsdata['status']

def getGPS_altitude(gps_poller):
    if gps_poller.gpsdata['status'] == "FIX":
        return gps_poller.gpsdata['altitude']
    else:
        return gps_poller.gpsdata['status']


# Get movement data
def getMovement_Accelerometer():
    acc, mag = MOVE_SENSOR.read()
    acc_x, acc_y, acc_z = acc
    mag_x, mag_y, mag_z, ord = mag
    return round(acc_x, -1), round(acc_y, -1)


## Run external commands, returns output
def _run_cmd(cmd):
    running_process = Popen(cmd, shell=True, stdout=PIPE)
    output = running_process.communicate()[0]
    return output
