import asyncore
import socket
from random import randrange
import time


HOST = 'localhost'
PORT = 5005
BUFFER = 1024

class DispatchHandler(asyncore.dispatcher_with_send):
    def __init__(self, socket, mainwindow):
        self.mainwindow = mainwindow
        asyncore.dispatcher_with_send.__init__(self, socket)

    def handle_read(self):
	data = self.recv(BUFFER)
        if data is not None:
            print "INPUT -- " + str(data)
            _TranslateToPanels(data, self.mainwindow)
	    vehicle_data = _GetVehicleData(data, self.mainwindow)
            
            if vehicle_data is not None:  	   
	      print "RETURN --  " + str(vehicle_data)
              self.send(str(vehicle_data))


class DispatchServer(asyncore.dispatcher):
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow

        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((HOST, PORT))
        self.listen(5)

    def handle_accept(self):
        connection = self.accept()
        if connection is not None:
            socket, address = connection
            print 'Incoming connection from' + str(address)
            handler = DispatchHandler(socket, self.mainwindow)


def _TranslateToPanels(data, mainwindow):
    data = str(data).split(";")
    for packet in data:

        if len(packet) >= 5 and packet.find(",") >= 0:
            type, name, xvalue, yvalue = packet.split(",")

            if name == "thr":
                mainwindow.tpos_text.SetLabel(xvalue)
 	    elif name == "brk":
                mainwindow.brake_text.SetLabel(xvalue)
 	    elif name == "dir":
                mainwindow.dpos_text.SetLabel(xvalue)
 	    elif name == "gim":
                mainwindow.gimx_text.SetLabel(xvalue)
                mainwindow.gimy_text.SetLabel(yvalue)


def _GetVehicleData(data, mainwindow):
    bat1_value = str(mainwindow.slider_bat1.GetValue())    
    bat2_value = str(mainwindow.slider_bat2.GetValue())    
    wifi_value = str(mainwindow.slider_wifi.GetValue())    
    rdelay_value = float(mainwindow.slider_rdelay.GetValue())



    data = str(data).split(";")
    for packet in data:

        if len(packet) >= 5 and packet.find(",") >= 0:
            type, name, xvalue, yvalue = packet.split(",")

            if name == "ka":
              if rdelay_value != 0:
                time.sleep(rdelay_value/1000)

              return(wifi_value + ',' + bat1_value + ',' + bat2_value)

