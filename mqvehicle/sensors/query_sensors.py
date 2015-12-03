import math
from random import randrange
from subprocess import *

import sensors.Adafruit_BMP085 as BMP085
import sensors.Adafruit_LSM303 as LSM303


#try:
    # Setup encironment sensor
ENV_SENSOR = BMP085.BMP085()

    # vehicle movement sensor
MOVEMENT_SENSOR = LSM303.Adafruit_LSM303(hires="false")
    
#except:
#    assert False, "Error: Failed to init sensors"

## Get data from vehicle components
def getBatteryA():
    try:
        return randrange(100)
    except:
        return False

def getBatteryB():
    try:
        return randrange(100)
    except:
        return False
    
def getWifi():
    wifi_value = -10

    try:
        wifi_value = 100 + int(wifi_value)
        return wifi_value

    except:
        return 0

## Get environment data
def getEnvironment_temperature():
    try:
        temperature = ENV_SENSOR.readTemperature()
        return temperature
    except:
        return False

def getEnvironment_humidity():
    try:
        return randrange(100)
    except:
        return False 

def getEnvironment_pressure():
    try:
        pressure = ENV_SENSOR.readPressure()
        return pressure
    except:
        return False

## Get GPS data
def getGPS_lat(gps_poller):
    try:
        if gps_poller.gpsdata['status'] == "FIX":
            return gps_poller.gpsdata['latitude']
        else:
            return gps_poller.gpsdata['status']
    except:
        return False

def getGPS_long(gps_poller):
    try:
        if gps_poller.gpsdata['status'] == "FIX":
            return gps_poller.gpsdata['longitude']
        else:
            return gps_poller.gpsdata['status']
    except:
        return False

def getGPS_speed(gps_poller):
    try:
        if gps_poller.gpsdata['status'] == "FIX":
            return math.floor(gps_poller.gpsdata['speed'])
        else:
            return gps_poller.gpsdata['status']
    except:
            return False

def getGPS_altitude(gps_poller):
    try:
        if gps_poller.gpsdata['status'] == "FIX":
            return gps_poller.gpsdata['altitude']
        else:
            return gps_poller.gpsdata['status']
    except:
        return False

# Get movement data
def getMovement_Accelerometer():
    try:   
        acc, mag = MOVEMENT_SENSOR.read()
        acc_x, acc_y, acc_z = acc
        mag_x, mag_y, mag_z, ord = mag

        return(round(acc_x, -1), round(acc_y, -1))

    except:
        return False


## Run external commands, returns output
def _run_cmd(cmd):
    try:
        running_process = Popen(cmd, shell=True, stdout=PIPE)
        output = running_process.communicate()[0]
        return output

    except:
        return False

