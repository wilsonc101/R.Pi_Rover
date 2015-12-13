import ConfigParser
from PyQt4 import QtCore
import json
import pika


config = ConfigParser.ConfigParser()
config.read('pi_controls.cfg')

CONTROL_EXCHANGE = config.get('control_exchange', 'name')
CONTROL_SERVER = config.get('control_exchange', 'server')

VEHICLE_EXCHANGE = config.get('vehicle_exchange', 'name')
VEHICLE_SERVER = config.get('vehicle_exchange', 'server')

VEHICLE_ID = config.get('vehicle_id', 'id')


class MQReader(QtCore.QThread):
    def __init__(self):
        try:
            QtCore.QThread.__init__(self)
            self.signal = QtCore.SIGNAL("signal")
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(CONTROL_SERVER))
            self.channel = self.connection.channel()

            ## EXCHANGE BASED ##
            self.channel.exchange_declare(exchange=CONTROL_EXCHANGE, type='topic')
            self.result = self.channel.queue_declare(exclusive=True)
            self.queue_name = self.result.method.queue
            
            self.channel.queue_bind(exchange=CONTROL_EXCHANGE, 
                                    queue=self.queue_name, 
                                    routing_key=VEHICLE_ID)
            self.channel.basic_consume(self._poll_queue, 
                                       queue=self.queue_name, 
                                       no_ack=True)

        except:
            assert False, "Error: Failed to connect to broker"


    def _poll_queue(self, ch, method, properties, body):
        try:
            self.emit(self.signal, str(body))
            return True
        except:
            return False

    def run(self):
        try:
            self.channel.start_consuming()
        except:
            return False


def sendControl(qt_window):
    # Enviroment
    temperature_value = qt_window.sb_temperature.value()
    humidity_value = qt_window.sb_humidity.value()
    pressure_value = qt_window.sb_pressure.value()

    # GPS
    north_value = qt_window.sb_north.value()
    east_value = qt_window.sb_east.value()


    # Create/populate JSON data structure
    data = {}
    data['environment'] = {'temperature': temperature_value, 'humidity': humidity_value}
    data['GPS'] = {'logitude': north_value, 'latitude': east_value}


    try:
        # Establish queue for writing
        connection = pika.BlockingConnection(pika.ConnectionParameters(VEHICLE_SERVER))
        channel = connection.channel()

        ## EXCHANGE BASED ##
        channel.exchange_declare(exchange=VEHICLE_EXCHANGE, type='topic')
        # Write JSON data to queue
        channel.basic_publish(exchange=VEHICLE_EXCHANGE, 
                              routing_key=VEHICLE_ID, 
                              body=json.dumps(data))
        connection.close()
        return True
     
    except:
        return False



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

