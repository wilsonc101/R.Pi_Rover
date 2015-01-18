from subprocess import *
from random import randrange


## Get data from vehicle components
def getBatteryA():
    return(randrange(100))

def getBatteryB():
    return(randrange(100))

def getWifi():
 #   return(randrange(100))

    getwifidata_cmd = "awk 'NR==3 {print $3}' /proc/net/wireless | cut -c 1-2"
    wifi_value = _run_cmd(getwifidata_cmd)

    if type(wifi_value) is not int:
        return(0)
    else:
        return(wifi_value)



## Get environment data
def getEnvironment_temperature():
    return(randrange(100))

def getEnvironment_humidity():
    return(randrange(100))

def getEnvironment_pressure():
    return(randrange(100))



## Get GPS data
def getGPS_north():
    return(randrange(100))

def getGPS_east():
    return(randrange(100))

def getGPS_speed():
    return(randrange(100))

def getGPS_altitude():
    return(randrange(100))





## Run external commands, returns output
def _run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output
