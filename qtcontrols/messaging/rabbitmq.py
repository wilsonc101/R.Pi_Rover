import ConfigParser
from PyQt4 import QtCore
import json
import pika


config = ConfigParser.ConfigParser()
config.read('pi_controls.cfg')

VEHICLE_ID = config.get('vehicle_id', 'id')

CONTROL_EXCHANGE = config.get('control_exchange', 'name')
CONTROL_SERVER = config.get('control_exchange', 'server')

VEHICLE_EXCHANGE = config.get('vehicle_exchange', 'name')
VEHICLE_SERVER = config.get('vehicle_exchange', 'server')

CAMERA_SERVER = config.get('camera_server', 'server')
CAMERA_PORT = config.get('camera_server', 'port')

class MQReader(QtCore.QThread):
    def __init__(self):
        self.vehicle_id = VEHICLE_ID
        self.control_exchange = CONTROL_EXCHANGE
        self.control_server = CONTROL_SERVER
        self.vehicle_exchange = VEHICLE_EXCHANGE
        self.vehicle_server = VEHICLE_SERVER

        try:
            QtCore.QThread.__init__(self)
            self.signal = QtCore.SIGNAL("signal")
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(VEHICLE_SERVER))
            self.channel = self.connection.channel()

            ## EXCHANGE BASED ##
            self.channel.exchange_declare(exchange=VEHICLE_EXCHANGE, 
                                          type='topic')
            
            self.result = self.channel.queue_declare(exclusive=True)
            self.queue_name = self.result.method.queue

            self.channel.queue_bind(exchange=VEHICLE_EXCHANGE,
                                    queue=self.queue_name,
                                    routing_key=VEHICLE_ID)
            
            self.channel.basic_consume(self._poll_queue,
                                       queue=self.queue_name,
                                       no_ack=True)

        except:
            raise SystemExit("Could not connect to queue server")


    def _poll_queue(self, ch, method, properties, body):
        try:
            self.emit(self.signal, str(body))
        except:
            return False

    def run(self):
        try:
            self.channel.start_consuming()

        except:
            return False


def MQWriter(qt_window):

    forward_value = qt_window.bar_forward.value()
    reverse_value = qt_window.bar_reverse.value()
    right_value = qt_window.bar_right.value()
    left_value = qt_window.bar_left.value()
    brake_value = qt_window.cb_brake.isChecked()

    cam_tilt_value = qt_window.slider_cam_tilt.value()
    cam_pan_value = qt_window.dial_cam_pan.value()

    veh_light_value = qt_window.cb_veh_light.isChecked()
    cam_light_value = qt_window.cb_cam_light.isChecked()

    shutdown_vehicle = qt_window.poweroff


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
    data['vehicle'] = {'direction': direction_value, 
                       'throttle': throttle_value, 
                       'brake': brake_value, 
                       'light': veh_light_value}
    
    data['camera'] = {'tilt': cam_tilt_value, 
                      'pan': cam_pan_value, 
                      'light': cam_light_value}
    
    data['state'] = {'shutdown': shutdown_vehicle}

    try:
        # Establish queue for writing
        connection = pika.BlockingConnection(pika.ConnectionParameters(CONTROL_SERVER))
        channel = connection.channel()

        ## EXCHANGE BASED ##
        channel.exchange_declare(exchange=CONTROL_EXCHANGE, type='topic')
        # Write JSON data to queue
        channel.basic_publish(exchange=CONTROL_EXCHANGE, 
                              routing_key=VEHICLE_ID, 
                              body=json.dumps(data))

        connection.close()

    except:
        return False