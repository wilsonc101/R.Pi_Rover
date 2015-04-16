import math

from subprocess import *
from random import randrange

import Adafruit_BMP085 as BMP085
import Adafruit_LSM303 as LSM303


# Setup encironment sensor
environment_sensor = BMP085.BMP085()

# vehicle movement sensor
movement_sensor = LSM303.Adafruit_LSM303(hires="false")

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
    temperature = environment_sensor.readTemperature()
    return(temperature)

def getEnvironment_humidity():
    return(randrange(100))

def getEnvironment_pressure():
    pressure = environment_sensor.readPressure()
    return(pressure)



## Get GPS data
def getGPS_lat(gps_poller):
    if gps_poller.gpsdata['status'] == "FIX":
        return gps_poller.gpsdata['latitude']
    else:
        return(gps_poller.gpsdata['status'])

def getGPS_long(gps_poller):
    if gps_poller.gpsdata['status'] == "FIX":
        return gps_poller.gpsdata['longitude']
    else:
        return(gps_poller.gpsdata['status'])

def getGPS_speed(gps_poller):
    if gps_poller.gpsdata['status'] == "FIX":
        return math.floor(gps_poller.gpsdata['speed'])
    else:
        return(gps_poller.gpsdata['status'])

def getGPS_altitude(gps_poller):
    if gps_poller.gpsdata['status'] == "FIX":
        return gps_poller.gpsdata['altitude']
    else:
        return(gps_poller.gpsdata['status'])


# Get movement data
def getMovement_Accelerometer():
        acc, mag = movement_sensor.read()
        acc_x, acc_y, acc_z = acc
        mag_x, mag_y, mag_z, ord = mag
        return(acc_x, acc_y)


## Run external commands, returns output
def _run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output


