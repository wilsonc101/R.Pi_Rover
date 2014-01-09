import socket
import time
import ConfigParser
import sys

# Set socket timeout
socket.setdefaulttimeout(2)

config = ConfigParser.ConfigParser()
config.read('pi_controls.cfg')

# Get servo names from config as arrays
[config.get('servos', 'direction_type'), config.get('servos', 'direction_name')]


def net_test(type,channel,value1,value2=0):
	# Test harness for net_send
	print(type,channel,value1,value2)


def net_connect():
	# Create network socket and return if successul (false string if not)
        HOST = config.get('network', 'vehicle_ip')
        PORT = int(config.get('network', 'vehicle_port'))
        net_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		net_socket.connect((HOST, PORT))
		print("Connected to " + HOST)
		return(net_socket)

	except:
       	        print("Network Connection Failed")
		return("False")



def net_send(socket,type,channel,value1,value2=0):
	# Send args to socket and output to stdout, return false string if socket non-functional
        try:
	        socket.sendall(str(type) + "," + channel + "," + str(value1) + "," + str(value2) + ";")
                print(str(type) + "," + channel + "," + str(value1) + "," + str(value2) + ";")
        except:
                print("Network Connection Error - Transmit")
		return("False")



