from PyQt4 import QtCore

import time
import pika
import json


class MQReader(QtCore.QThread):
    def __init__(self, queue, mqhost):
        QtCore.QThread.__init__(self)
        self.signal = QtCore.SIGNAL("signal")
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(mqhost))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.channel.basic_consume(self._poll_queue, queue=queue)


    def _poll_queue(self, ch, method, properties, body):
        self.emit(self.signal, str(body))
        ch.basic_ack(delivery_tag = method.delivery_tag)


    def run(self):
        self.channel.start_consuming()


def MQWriter(qt_window, queue, mqhost):

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
        connection = pika.BlockingConnection(pika.ConnectionParameters(mqhost))
        channel = connection.channel()
        channel.queue_declare(queue=queue)

        # Write JSON data to queue
        channel.basic_publish(exchange='',routing_key=queue, body=json.dumps(data))
        connection.close()

    except:
        raise SystemExit("Could not write to control queue")





