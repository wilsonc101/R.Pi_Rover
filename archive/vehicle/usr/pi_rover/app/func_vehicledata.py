from subprocess import *
from random import randrange

## Get data from vehicle components
def GetVehicleData(metric):

	if metric == "batt1":
		data = str(randrange(100))

	if metric == "batt2":
		data = str(randrange(100))

	if metric == "wifi":
		# Extract signal info from wireless proc file 
		getwifidata_cmd = "awk 'NR==3 {print $3}' /proc/net/wireless | cut -c 1-2"
		data = _run_cmd(getwifidata_cmd)

        return(str(data))


## Run external commands, returns output
def _run_cmd(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate()[0]
        return output
