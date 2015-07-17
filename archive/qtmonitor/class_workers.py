import ConfigParser
from PyQt4 import QtCore
import json
import pika
import time


class MQReader(QtCore.QThread):
    def __init__(self, q_name, q_server):
#        try:   
            print "Q: " + q_name + " -- Server: " + q_server
            QtCore.QThread.__init__(self)
            self.signal = QtCore.SIGNAL("signal")
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(q_server))
            self.channel = self.connection.channel()

            ## EXCHANGE BASED ##
            self.channel.exchange_declare(exchange=q_name, type='fanout')
            self.result = self.channel.queue_declare(exclusive=True)
            self.queue_name = self.result.method.queue
  
            self.channel.queue_bind(exchange=q_name, queue=self.queue_name)
            self.channel.basic_consume(self._poll_queue, queue=self.queue_name, no_ack=True)

#        except:
#            raise SystemExit("Could not connect to queue server")


    def _poll_queue(self, ch, method, properties, body):
        try:
            self.emit(self.signal, str(body))

        except:
            raise SystemExit("Error polling vehicle queue")


    def run(self):
        try:
            self.channel.start_consuming()

        except:
            raise SystemExit("Lost connection to queue server")


def GUIUpdate(qt_window, json_data):
    if 'vehicle' in json_data:
        if 'throttle' in json_data['vehicle']: qt_window.slider_throttle.setValue(int(json_data['vehicle']['throttle']))
        if 'direction' in json_data['vehicle']: qt_window.slider_direction.setValue(int(json_data['vehicle']['direction']))
        if 'brake' in json_data['vehicle']: qt_window.rb_brake.setChecked(json_data['vehicle']['brake'])
        if 'wifi' in json_data['vehicle']: qt_window.tb_wifi.setText(str(json_data['vehicle']['wifi']))
        if 'batteryA' in json_data['vehicle']: qt_window.tb_batt_a.setText(str(json_data['vehicle']['batteryA']))
        if 'batteryB' in json_data['vehicle']: qt_window.tb_batt_b.setText(str(json_data['vehicle']['batteryB']))


    if 'camera' in json_data:
        if 'tilt' in json_data['camera']: qt_window.slider_cam_tilt.setValue(int(json_data['camera']['tilt']))
        if 'pan' in json_data['camera']: qt_window.dial_cam_pan.setValue(int(json_data['camera']['pan']))


    if 'environment' in json_data:
        if 'temperature' in json_data['environment']: qt_window.tb_temperature.setText(str(json_data['environment']['temperature']))
        if 'humidity' in json_data['environment']: qt_window.tb_humidity.setText(str(json_data['environment']['humidity']))
        if 'pressure' in json_data['environment']: qt_window.tb_pressure.setText(str(json_data['environment']['pressure']))

    if 'GPS' in json_data:
        if 'north' in json_data['GPS']: qt_window.tb_north.setText(str(json_data['GPS']['north']))
        if 'east' in json_data['GPS']: qt_window.tb_east.setText(str(json_data['GPS']['east']))
        if 'speed' in json_data['GPS']: qt_window.tb_speed.setText(str(json_data['GPS']['speed']))
        if 'altitude' in json_data['GPS']: qt_window.tb_altitude.setText(str(json_data['GPS']['altitude']))




