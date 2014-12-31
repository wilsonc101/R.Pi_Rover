from PyQt4 import QtCore

import time
import pika
import json
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('pi_controls.cfg')

QUEUE_SERVER = config.get('queue_server', 'server')
CONTROL_QUEUE = config.get('control_queue', 'name')
VEHICLE_QUEUE = config.get('vehicle_queue', 'name')


class MQReader(QtCore.QThread):
    def __init__(self):
        self.queue_server = QUEUE_SERVER
        self.control_queue = CONTROL_QUEUE
        self.vehicle_queue = VEHICLE_QUEUE

        try:   
            QtCore.QThread.__init__(self)
            self.signal = QtCore.SIGNAL("signal")
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(QUEUE_SERVER))
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
        connection = pika.BlockingConnection(pika.ConnectionParameters(QUEUE_SERVER))
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
    if 'environment' in json_data:
        if 'temperature' in json_data['environment']: qt_window.tb_temperature.setText(str(json_data['environment']['temperature']))
        if 'humidity' in json_data['environment']: qt_window.tb_humidity.setText(str(json_data['environment']['humidity']))

