import socket
import time
import ConfigParser


config = ConfigParser.ConfigParser()
config.read('pi_controls.cfg')

# Get servo names from config as arrays
[config.get('servos', 'direction_type'), config.get('servos', 'direction_name')]


def net_test(type,channel,value1,value2=0):
	print(type,channel,value1,value2)



def net_connect():
        HOST = config.get('network', 'vehicle_ip')
        PORT = int(config.get('network', 'vehicle_port'))
        net_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#        net_socket_state = False

 #       while net_socket_state == False:
	try:
		net_socket.connect((HOST, PORT))
#                        net_socket_state = True
		return(net_socket)
                        #frame.panel_connection.SetBackgroundColour("green")
                        #frame.FrameUpdate()

	except:
		return("False")
#        	        print("Network Connection Failed")
#                        net_socket_state = False
#                        frame.panel_connection.SetBackgroundColour("red")
#                        frame.FrameUpdate()
#                        time.sleep(2)


def net_disconnect():
        global net_socket

        net_socket.close()


def net_send(socket,type,channel,value1,value2=0):
        global net_socket

        try:
                socket.sendall(str(type) + "," + channel + "," + str(value1) + "," + str(value2) + ";")
                print(str(type) + "," + channel + "," + str(value1) + "," + str(value2) + ";")
        except:
                print("Network Connection Error - Transmit")
                net_connect()
#
