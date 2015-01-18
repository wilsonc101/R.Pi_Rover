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
#        try:   
            QtCore.QThread.__init__(self)
            self.signal = QtCore.SIGNAL("signal")
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(CONTROL_SERVER))
            self.channel = self.connection.channel()

            ## EXCHANGE BASED ##
            self.channel.exchange_declare(exchange=CONTROL_QUEUE, type='fanout')
            self.result = self.channel.queue_declare(exclusive=True)
            self.queue_name = self.result.method.queue
  
            self.channel.queue_bind(exchange=CONTROL_QUEUE, queue=self.queue_name)
            self.channel.basic_consume(self._poll_queue, queue=self.queue_name, no_ack=True)


            ## QUEUE BASED ##
#            self.channel.queue_declare(queue=CONTROL_QUEUE)
#            self.channel.basic_consume(self._poll_queue, queue=CONTROL_QUEUE)

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


def MQWriter(qt_window):
    # Enviroment
    temperature_value = qt_window.sb_temperature.value()
    humidity_value = qt_window.sb_humidity.value()
 
    # GPS
    north_value = qt_window.sb_north.value()
    east_value = qt_window.sb_east.value()

 
    # Create/populate JSON data structure
    data = {}
    data['environment'] = {'temperature': temperature_value, 'humidity': humidity_value}
    data['GPS'] = {'north': north_value, 'east': east_value}


    try:
        # Establish queue for writing
        connection = pika.BlockingConnection(pika.ConnectionParameters(VEHICLE_SERVER))
        channel = connection.channel()

        ## EXCHANGE BASED ##
        channel.exchange_declare(exchange=VEHICLE_QUEUE, type='fanout')
        # Write JSON data to queue
        channel.basic_publish(exchange=VEHICLE_QUEUE, routing_key='', body=json.dumps(data))



        ## QUEUE BASED ##
#        channel.queue_declare(queue=VEHICLE_QUEUE)
        # Write JSON data to queue
#        channel.basic_publish(exchange='',routing_key=VEHICLE_QUEUE, body=json.dumps(data))


        connection.close()

    except:
        raise SystemExit("Could not write to control queue")



def GUIUpdate(qt_window, json_data):
    print json.dumps(json_data)
 
    if 'vehicle' in json_data:
        if 'throttle' in json_data['vehicle']: 
            qt_window.slider_throttle.setValue(int(json_data['vehicle']['throttle']))

        if 'direction' in json_data['vehicle']: 
            qt_window.slider_direction.setValue(int(json_data['vehicle']['direction']))

        if 'brake' in json_data['vehicle']: 
            qt_window.rb_brake.setChecked(json_data['vehicle']['brake'])



    if 'camera' in json_data:
        if 'tilt' in json_data['camera']: 
            qt_window.slider_cam_tilt.setValue(int(json_data['camera']['tilt']))

        if 'pan' in json_data['camera']: 
            qt_window.dial_cam_pan.setValue(int(json_data['camera']['pan']))
