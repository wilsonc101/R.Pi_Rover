import socket
import time
import ConfigParser
import sys

import controls_logging as log

# Set socket timeout
socket.setdefaulttimeout(2)

config = ConfigParser.ConfigParser()
config.read('pi_controls.cfg')

logfile = log.CreateLogger(console=1, file=1, filepath='pi_rover.log', level=config.get('logging', 'level'))

def net_test(type,channel,value1,value2=0):
	# Test harness for net_send
	logfile.debug(str(type) + "," + str(channel) + ","+ str(value1) + "," + str(value2))

def net_connect():
	# Create network socket and return if successul (false string if not)
        HOST = config.get('network', 'vehicle_ip')
        PORT = int(config.get('network', 'vehicle_port'))
        net_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		net_socket.connect((HOST, PORT))
		logfile.warning("connected to " + str(HOST))
		return(net_socket)

	except:
       	        logfile.warning("network connection failed")
		return("False")



def net_send(socket,type,channel,value1,value2=0):
	# Send args to socket and output to stdout, return false string if socket non-functional
        try:
	        socket.sendall(str(type) + "," + channel + "," + str(value1) + "," + str(value2) + ";")
        except:
                logfile.warning("network connection error - Transmit")
		return("False")


def net_listen(socket):
	# Listen on existing connection for data returned from vehicle
	try:	
		while 1:
			data = socket.recv(1024)
	                if not data: break
		    	return(data)
                logfile.warning("network connection error - Receive")
		return("False")  

	except:
                logfile.warning("network connection error - Receive")
		return("False")  
