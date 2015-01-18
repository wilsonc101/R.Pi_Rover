from PyQt4 import QtCore

import time
import pika
import json
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('pi_controls.cfg')

CONTROL_QUEUE = config.get('control_queue', 'name')
CONTROL_SERVER = config.get('control_queue', 'server')

VEHICLE_QUEUE = config.get('vehicle_queue', 'name')
VEHICLE_SERVER = config.get('vehicle_queue', 'server')


class MQReader(QtCore.QThread):
    def __init__(self):
        self.control_queue = CONTROL_QUEUE
        self.control_server = CONTROL_SERVER
        self.vehicle_queue = VEHICLE_QUEUE
        self.vehicle_server = VEHICLE_SERVER

        try:   
            QtCore.QThread.__init__(self)
            self.signal = QtCore.SIGNAL("signal")
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(VEHICLE_SERVER))
            self.channel = self.connection.channel()

            ## EXCHANGE BASED ##
            self.channel.exchange_declare(exchange=VEHICLE_QUEUE, type='fanout')
            self.result = self.channel.queue_declare(exclusive=True)
            self.queue_name = self.result.method.queue

            self.channel.queue_bind(exchange=VEHICLE_QUEUE, queue=self.queue_name)
            self.channel.basic_consume(self._poll_queue, queue=self.queue_name, no_ack=True)

            ## QUEUE BASED ##
#            self.channel.queue_declare(queue=VEHICLE_QUEUE)
#            self.channel.basic_consume(self._poll_queue, queue=VEHICLE_QUEUE)
 
        except:
            raise SystemExit("Could not connect to queue server")


    def _poll_queue(self, ch, method, properties, body):
        try:
            self.emit(self.signal, str(body))
#            ch.basic_ack(delivery_tag = method.delivery_tag)
        except:
            raise SystemExit("Error polling vehicle queue")

    def run(self):
        try:
            self.channel.start_consuming()

        except:
            raise SystemExit("Lost connection to queue server")


def MQWriter(qt_window):

    forward_value = qt_window.bar_forward.value()
    reverse_value = qt_window.bar_reverse.value()
    right_value = qt_window.bar_right.value()
    left_value = qt_window.bar_left.value()
    brake_value = qt_window.rb_brake.isChecked()
 
    cam_tilt_value = qt_window.slider_cam_tilt.value()
    cam_pan_value = qt_window.dial_cam_pan.value()
 

    # Invert value for left (left = -100 to 0, right = 0 to 100)
    if left_value > 0:
        direction_value = 0 - left_value
    else: 
        direction_value = right_value 

    # Invert value for reverse (reverse = -100 to 0, forward = 0 to 100)
    if reverse_value > 0:
        throttle_value = 0 - reverse_value
    else: 
        throttle_value = forward_value 
       
    # Transform 0 to 100 slider/dial values to -100 to 100 range
    cam_tilt_value = (cam_tilt_value*2)-100
    cam_pan_value = (cam_pan_value*2)-100


    # Create/populate JSON data structure
    data = {}
    data['vehicle'] = {'direction': direction_value, 'throttle': throttle_value, 'brake': brake_value}
    data['camera'] = {'tilt': cam_tilt_value, 'pan': cam_pan_value}



    try:
        # Establish queue for writing
        connection = pika.BlockingConnection(pika.ConnectionParameters(CONTROL_SERVER))
        channel = connection.channel()

        ## EXCHANGE BASED ##
        channel.exchange_declare(exchange=CONTROL_QUEUE, type='fanout')
        # Write JSON data to queue
        channel.basic_publish(exchange=CONTROL_QUEUE, routing_key='', body=json.dumps(data))


        ## QUEUE BASED ##
#        channel.queue_declare(queue=CONTROL_QUEUE)
        # Write JSON data to queue
#        channel.basic_publish(exchange='',routing_key=CONTROL_QUEUE, body=json.dumps(data))


        connection.close()

    except:
        raise SystemExit("Could not write to control queue")



def GUIUpdate(qt_window, json_data):
    if 'vehicle' in json_data:
        if 'wifi' in json_data['vehicle']: qt_window.bar_wifi.setValue(int(json_data['vehicle']['wifi']))
        if 'batteryA' in json_data['vehicle']: qt_window.bar_battery_a.setValue(int(json_data['vehicle']['batteryA']))
        if 'batteryB' in json_data['vehicle']: qt_window.bar_battery_b.setValue(int(json_data['vehicle']['batteryB']))
  

    if 'environment' in json_data:
        if 'temperature' in json_data['environment']: qt_window.tb_temperature.setText(str(json_data['environment']['temperature']))
        if 'humidity' in json_data['environment']: qt_window.tb_humidity.setText(str(json_data['environment']['humidity']))
        if 'pressure' in json_data['environment']: qt_window.tb_pressure.setText(str(json_data['environment']['pressure']))

    if 'GPS' in json_data:
        if 'north' in json_data['GPS']: qt_window.tb_gps_north.setText(str(json_data['GPS']['north']))
        if 'east' in json_data['GPS']: qt_window.tb_gps_east.setText(str(json_data['GPS']['east']))
        if 'speed' in json_data['GPS']: qt_window.tb_gps_speed.setText(str(json_data['GPS']['speed']))
        if 'altitude' in json_data['GPS']: qt_window.tb_gps_altitude.setText(str(json_data['GPS']['altitude']))



