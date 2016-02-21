#!/usr/bin/python -B

import sys
import os
import ConfigParser
import argparse
import json
import multiprocessing
import time

import core.logger as log
import messaging.rmq as rmq
import messaging.redisdb as rdb
import vehicle.rover as rover

# Setup input arguments
arg_parser = argparse.ArgumentParser(description='Usage options for aws_init')
arg_parser.add_argument('-c', '--configfile', help="Optional - configuration file path")
arg_parser.add_argument('-l', '--logfile', help="Optional - Log file path")
arg_parser.add_argument('-v', '--vehicleid', help="Optional - override default vehicle ID")

# Process input and generate dict
args = vars(arg_parser.parse_args())


# Validate input - Config file
if args['configfile'] is not None:
    configfilepath = args['configfile']
else:
    local_path = os.path.dirname(os.path.abspath(__file__))
    configfilepath = str(local_path) + '/config/offline_mapping.cfg'

# Get config
try:
    assert os.path.isfile(configfilepath), "Error: Config file does not exist"

    config = ConfigParser.ConfigParser()
    config.read(configfilepath)
except:
    raise SystemExit("FATAL: Unknown error 001 - " + str(sys.exc_info()[0]))


# Validate input - Log file
if args['logfile'] is not None:
    logfilepath = args['logfile']
else:
    logfilepath = config.get('logging', 'path')    

# Setup logging
try:
    logfile = log.CreateLogger(toconsole=False, tofile=True, filepath=logfilepath, level=config.get('logging', 'level'))
    assert logfile, "Error: Failed to create log outputs"

except:
    raise SystemExit("FATAL: Unknown error 002 - " + str(sys.exc_info()[0]))

# Validate input - vehicle id
if args['vehicleid'] is not None:
    RMQ_TOPIC = args['vehicleid']
else:
    RMQ_TOPIC = config.get('platform_broker', 'unit_id')


# Validate config
try:
    REDIS_HOST = config.get('redis', 'host')
    REDIS_PORT = int(config.get('redis', 'port'))
    REDIS_DB = int(config.get('redis', 'db'))
    
    RMQ_HOST_CONTROL = config.get('platform_broker', 'control_server')
    RMQ_PORT_CONTROL = int(config.get('platform_broker', 'control_port'))
    RMQ_EXCHANGE_CONTROL = config.get('platform_broker', 'control_exchange')

    RMQ_HOST_VEHICLE = config.get('platform_broker', 'vehicle_server')
    RMQ_PORT_VEHICLE = int(config.get('platform_broker', 'vehicle_port'))
    RMQ_EXCHANGE_VEHICLE = config.get('platform_broker', 'vehicle_exchange')

    logfile.debug("Configuration file loaded")

except ConfigParser.NoSectionError as err:
    logfile.error("Error: " + str(err))
    raise SystemExit("Error: " + str(err))

except ConfigParser.NoOptionError as err:
    logfile.error("Error: " + str(err))
    raise SystemExit("Error: " + str(err))

except:
    raise SystemExit("FATAL: Unknown error 003 - " + str(sys.exc_info()[0]))

# Global vars
VEHICLE_DATA = rover.piRoverVehicle()
CONTROL_DATA = rover.piRoverControls()

def _processRMQInput(data):
# Populate global var from RMQ JSON messages - return tuple of messages (for SQS, for RMQ)
    logfile.debug("Received data from RMQ: " + str(data))
    try:
        json_data = json.loads(data)

        # NON RETURNING (ingest only)
        if 'camera' in json_data:
            if 'tilt' in json_data['camera']: CONTROL_DATA.cameraTiltPosition = int(json_data['camera']['tilt'])
            if 'pan' in json_data['camera']: CONTROL_DATA.cameraPanPosition = int(json_data['camera']['pan'])
            if 'light' in json_data['camera']: CONTROL_DATA.cameraLightState = json_data['camera']['light']

        if 'vehicle' in json_data:
            if 'throttle' in json_data['vehicle']: CONTROL_DATA.throttlePosition = json_data['vehicle']['throttle']
            if 'direction' in json_data['vehicle']: CONTROL_DATA.directionPosition = json_data['vehicle']['direction']
            if 'brake' in json_data['vehicle']: CONTROL_DATA.brakeState = json_data['vehicle']['brake']
            if 'light' in json_data['vehicle']: CONTROL_DATA.vehicleLightState = json_data['vehicle']['light']
            if 'wifi' in json_data['vehicle']: VEHICLE_DATA.vehicleWifi = json_data['vehicle']['wifi']
            if 'batteryA' in json_data['vehicle']: VEHICLE_DATA.vehicleBatteryA = json_data['vehicle']['batteryA']
            if 'batteryB' in json_data['vehicle']: VEHICLE_DATA.vehicleBatteryB = json_data['vehicle']['batteryB']

        if 'environment' in json_data:
            if 'temperature' in json_data['environment']: VEHICLE_DATA.environmentTemperature = json_data['environment']['temperature']
            if 'humidity' in json_data['environment']: VEHICLE_DATA.environmentHumidity = json_data['environment']['humidity']
            if 'pressure' in json_data['environment']: VEHICLE_DATA.environmentPressure = json_data['environment']['pressure']

        if 'GPS' in json_data:
            if 'latitude' in json_data['GPS']: VEHICLE_DATA.gpsLatitude = json_data['GPS']['latitude']
            if 'longitude' in json_data['GPS']: VEHICLE_DATA.gpsLongitude = json_data['GPS']['longitude']
            if 'speed' in json_data['GPS']: VEHICLE_DATA.gpsSpeed = json_data['GPS']['speed']
            if 'altitude' in json_data['GPS']: VEHICLE_DATA.gpsAltitude = json_data['GPS']['altitude']

        if 'accelerometer' in json_data:
            if 'x' in json_data['accelerometer']: VEHICLE_DATA.accelLR = json_data['accelerometer']['x']
            if 'y' in json_data['accelerometer']: VEHICLE_DATA.accelRF = json_data['accelerometer']['y']

        # RETURNING (bi-directional)
        if 'camera' in json_data:
            print json_data['camera']
            if 'still' in json_data['camera']: return(_processCameraStill(json_data['camera']['still']), None)

        return (None, None)

    except:
        return False


def _GenerateVehicleStatusMessage():
# Post data from globals to SQS
    if CONTROL_DATA.throttlePosition is None: throttle_position = 0
    if CONTROL_DATA.directionPosition is None: direction_position = 0

    post_data = {'vehicle_id': RMQ_TOPIC,
                 'latitude': VEHICLE_DATA.gpsLatitude, 
                 'longitude': VEHICLE_DATA.gpsLongitude,
                 'altitude': VEHICLE_DATA.gpsAltitude,
                 'throttle': throttle_position,
                 'direction': direction_position}

    return post_data


def main():

    #### SETUP REDIS CONNECTION
    redis_client = rdb.redisdbConnection(host=REDIS_HOST, 
                                         port=REDIS_PORT, 
                                         db=REDIS_DB) 
    
    #### SETUP RABBITMQ CONNECTIONS
    ## Control
    # Reader
    rmq_control_pconn, rmq_control_cconn = multiprocessing.Pipe()
    rmq_control_reader = rmq.rmqClientReader(host=RMQ_HOST_CONTROL, port=RMQ_PORT_CONTROL, log=logfile)

    if rmq_control_reader.connected == False:
        raise SystemExit("FATAL: Failed to connect to RQM broker")
    logfile.info("Connected to RMQ server - control")

    rmq_control_reader.subscribe(RMQ_EXCHANGE_CONTROL, RMQ_TOPIC)
    logfile.info("Subscribed to RMQ control topic " + RMQ_TOPIC)

    rmq_control_thread = multiprocessing.Process(target=rmq_control_reader.run, args=(rmq_control_cconn,))
    rmq_control_thread.daemon = True
    rmq_control_thread.start()

    # Writer
    result = rmq_client_control_writer = rmq.rmqClientWriter(host=RMQ_HOST_CONTROL, port=RMQ_PORT_CONTROL, log=logfile)
    assert result, "Error connecting to RMQ broker for writing"
    result = rmq_client_control_writer.declareExchange(RMQ_EXCHANGE_CONTROL)
    assert result, "Error declaring RMQ exchange"


    ## Vehicle
    # Reader
    rmq_vehicle_pconn, rmq_vehicle_cconn = multiprocessing.Pipe()
    rmq_vehicle_reader = rmq.rmqClientReader(host=RMQ_HOST_VEHICLE, port=RMQ_PORT_VEHICLE)

    if rmq_vehicle_reader.connected == False:
        raise SystemExit("FATAL: Failed to connect to RQM broker")
    logfile.info("Connected to RMQ server - vehicle")
 
    rmq_vehicle_reader.subscribe(RMQ_EXCHANGE_VEHICLE, RMQ_TOPIC)
    logfile.info("Subscribed to RMQ vehicle topic " + RMQ_TOPIC)

    rmq_vehicle_thread = multiprocessing.Process(target=rmq_vehicle_reader.run, args=(rmq_vehicle_cconn,))
    rmq_vehicle_thread.daemon = True
    rmq_vehicle_thread.start()


    mapping_sub_counter = 0
    mapping_object_added = False
    
    while 1:
        # ~3s subloop
        ## Post messages to redis server
        if mapping_sub_counter == 30:
            mapping_sub_counter = 0
            status_message = _GenerateVehicleStatusMessage()
            
            print status_message
            
            if not mapping_object_added:
                redis_client.createObject(id=status_message['vehicle_id'],
                                          type="marker",
                                          lat=status_message['latitude'],
                                          long=status_message['longitude'])
            else:
                redis_client.updateObject(id=status_message['vehicle_id'],
                                          type="marker",
                                          lat=status_message['latitude'],
                                          long=status_message['longitude'])               

        # Control data
        if rmq_control_pconn.poll() == True: 
            logfile.debug("Recieved data from RMQ - control")
            result = _processRMQInput(rmq_control_pconn.recv())
            assert result, "Error: Failed processing RMQ control data"
            
        # Vehicle data
        if rmq_vehicle_pconn.poll() == True: 
            logfile.debug("Recieved data from RMQ - vehicle")
            result = _processRMQInput(rmq_vehicle_pconn.recv())
            assert result, "Error: Failed processing RMQ control data"

        mapping_sub_counter += 1
        time.sleep(.1)


if __name__ == '__main__':
    try: 
        main()
    except (KeyboardInterrupt, SystemExit) as err:
        logfile.info("User action - Exiting")
        print str(err) + " -- Exiting..."

    except AssertionError as err:
        print str(err)

    except:
        print "Error: unknown error 000 - " + str(sys.exc_info()[0])
