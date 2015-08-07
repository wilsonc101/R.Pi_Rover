#!/usr/bin/python -B

import sys
import os
import ConfigParser
import argparse
import boto3
import json
import time
import multiprocessing

import core.logger as log
import messaging.mqtt as mqtt
import messaging.edgware as edgware

# Setup input arguments
arg_parser = argparse.ArgumentParser(description='Usage options for aws_init')
arg_parser.add_argument('-c', '--configfile', help="Optional - configuration file path")
arg_parser.add_argument('-l', '--logfile', help="Optional - Log file path")
arg_parser.add_argument('-i', '--keyid', help="AWS access key ID ")
arg_parser.add_argument('-k', '--key', help="AWS access key")

# Process input and generate dict
args = vars(arg_parser.parse_args())


# Validate input - Config file
if args['configfile'] is not None:
    configfilepath = args['configfile']
else:
    local_path = os.path.dirname(os.path.abspath(__file__))
    configfilepath = str(local_path) + '/config/sqs_adaptor.cfg'

# Get config
try:
    assert os.path.isfile(configfilepath), "Error: Config file does not exist"

    config = ConfigParser.ConfigParser()
    config.read(configfilepath)
except:
    raise SystemExit("FATAL: Unknown error - " + str(sys.exc_info()[0]))


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
    raise SystemExit("FATAL: Unknown error - " + str(sys.exc_info()[0]))


# Validate input - access creds
if args['keyid'] is None: 
    raise SystemExit("Error: No key id provided")
else:
    AWS_KEY_ID = args['keyid']

if args['key'] is None: 
    raise SystemExit("Error: No key provided")
else:
    AWS_KEY = args['key']


# Validate config
try:
    AWS_DEFAULT_REGION = config.get('aws_defaults', 'region')
    AWS_DEFAULT_QUEUE_NAME = config.get('aws_defaults', 'queue_name')

    # Mosquitto connection details
    MQTT_HOST = config.get('edgware_broker', 'server')
    MQTT_PORT = int(config.get('edgware_broker', 'port'))
    MQTT_TOPIC_IN = config.get('edgware_broker', 'input_topic')
    MQTT_TOPIC_OUT = config.get('edgware_broker', 'output_topic')

    EDGWARE_PLATFORM_TEMPLATE_PATH = config.get('vehicle_template', 'path')

    logfile.debug("Configuration file loaded")

except ConfigParser.NoSectionError as err:
    logfile.error("Error: " + str(err))
    raise SystemExit("Error: " + str(err))

except ConfigParser.NoOptionError as err:
    logfile.error("Error: " + str(err))
    raise SystemExit("Error: " + str(err))

except:
    raise SystemExit("FATAL: Unknown error - " + str(sys.exc_info()[0]))

def writeMQTTOutput(client, topic, data):
    result = client.publish(topic=topic, payload=data)
    logfile.debug("Writing data to MQTT: " + str(data))
    assert result, "Error publishing MQTT message to " + str(topic)
    return(result)


def processSQSInput(attributes, message_attributes, body):
    platform_data = {}    

    # Message Attributes
    # Fail if no vehicle ID present
    if 'vehicle_id' in message_attributes:
        vehicle_id = message_attributes['vehicle_id']['StringValue']
    else:
        return False

    # Attributes
    platform_data['last_message_epoch'] = attributes['SentTimestamp']
    platform_data['sender'] = attributes['SenderId']
    
    # Body
    try:
        body_data = json.loads(body)
    except:
        return False

    for field in body_data:
        platform_data[field] = body_data[field]

    return((vehicle_id, platform_data))


def registerEdgwareTypes(mqtt_client):
    try:
        with open(EDGWARE_PLATFORM_TEMPLATE_PATH) as datafile:
            json_data = json.load(datafile)
    except:
        assert False, "Error: Failed to load JSON template"

    # Enumerate template and populate Edgware
    try:
        i = 100
        for service in json_data['services']:
            i += 1
            service_type = edgware.serviceType()
            service_type.type = json_data['services'][service]['type']
            service_type.mode = json_data['services'][service]['mode']
            service_type.correl = i
            
            message =  json.dumps(service_type.generateJSON())
            assert message, "Error generating JSON for service type " + str(json_data['services'][service]['type'])
            logfile.debug("Registering Edgware service type: " + str(json_data['services'][service]['type']))
            writeMQTTOutput(mqtt_client, MQTT_TOPIC_IN, message)
    
        i = 1000
        for system in json_data['systems']:
            i += 1
            system_type = edgware.systemType()
            system_type.type = json_data['systems'][system]['type']
            system_type.services = json_data['systems'][system]['services']
            system_type.correl = i

            message =  json.dumps(system_type.generateJSON())
            assert message, "Error generating JSON for system type " + str(json_data['systems'][system]['type'])
            logfile.debug("Registering Edgware service type: " + str(json_data['systems'][system]['type']))
            writeMQTTOutput(mqtt_client, MQTT_TOPIC_IN, message)
   
        i = 2000
        for platform in json_data['platforms']:
            i += 1
            platform_type = edgware.platformType()
            platform_type.type = json_data['platforms'][platform]['type']
            platform_type.correl = i

            message =  json.dumps(platform_type.generateJSON())
            assert message, "Error generating JSON for platform type " + str(json_data['platforms'][platform]['type'])
            logfile.debug("Registering Edgware service type: " + str(json_data['platforms'][platform]['type']))
            writeMQTTOutput(mqtt_client, MQTT_TOPIC_IN, message)

        return(True)

    except:
        logfile.error("Error: Unknown error caught when registering Edware types")
        return(False)


def registerNewPlatform(mqtt_client, vehicle_id):
    try:
        ## Define elements
        # Platforms
        platform = edgware.platform()
        platform.type = "simulation-platform"
        platform.id = vehicle_id
        platform.correl = 10001
        logfile.info("Edgware - Regsitering platform " + str(platform.id))
        writeMQTTOutput(mqtt_client, MQTT_TOPIC_IN, json.dumps(platform.generateJSON()))
 
        # Systems (+ activate)
        system = edgware.system()
        system.type = "vehicle"
        system.id = platform.id + "/vehicle"
        system.correl = 20001
        activate_system = json.dumps({"op":"state:system", "id": system.id, "state":"running", "correl":20002})
        logfile.info("Edgware - Regsitering system " + str(system.id))
        writeMQTTOutput(mqtt_client, MQTT_TOPIC_IN, json.dumps(system.generateJSON()))
        writeMQTTOutput(mqtt_client, MQTT_TOPIC_IN, activate_system)

        system = edgware.system()
        system.type = "control"
        system.id = platform.id + "/control"
        system.correl = 30001
        activate_system = json.dumps({"op":"state:system", "id": system.id, "state":"running", "correl":30002})
        logfile.info("Edgware - Regsitering system " + str(system.id))
        writeMQTTOutput(mqtt_client, MQTT_TOPIC_IN, json.dumps(system.generateJSON()))
        writeMQTTOutput(mqtt_client, MQTT_TOPIC_IN, activate_system)

        return True

    except:
        logfile.error("Error: Could not register vehicle " + vehicle_id)
        return False


def updatePlatformPosition(mqtt_client, vehicle_id, latitude, longitude, altitude):
    try:
        platform = edgware.platform()
        platform.type = "simulation-platform"
        platform.id = vehicle_id
        platform.loc['lat'] = latitude
        platform.loc['long'] = longitude
        platform.loc['alt'] = altitude
        platform.correl = 10001
        logfile.info("Edgware - Updating platform " + str(platform.id))
        writeMQTTOutput(mqtt_client, MQTT_TOPIC_IN, json.dumps(platform.generateJSON()))
        return True

    except:
        return False



known_platforms = {}
def main():

    #### Connect to AWS resources
    try:
        session = boto3.session.Session(aws_access_key_id=AWS_KEY_ID, 
                                        aws_secret_access_key=AWS_KEY, 
                                        region_name=AWS_DEFAULT_REGION)
        logfile.info("Connected to AWS")

    except:
        logfile.error("Error: Could not connect to AWS")
        assert False, "Error: Could not connect to AWS"

    sqs_client = session.client('sqs')
    queue_url = sqs_client.get_queue_url(QueueName=AWS_DEFAULT_QUEUE_NAME)['QueueUrl']

    sqs = session.resource('sqs')
    sqs_queue = sqs.Queue(queue_url)


    #### SETUP MQTT CONNECTION
    mqtt_reader_pconn, mqtt_reader_cconn = multiprocessing.Pipe()

    mqtt_client = mqtt.mqttClient(host=MQTT_HOST, 
                                  port=MQTT_PORT, 
                                  pipe=mqtt_reader_cconn, 
                                  client_id=("sqsadp"), 
                                  log=logfile)
    assert mqtt_client.connected, "FATAL: Failed to connect to MQTT broker"
    logfile.info("Connected to MQTT server")

    mqtt_client.subscribe(topic=MQTT_TOPIC_OUT)
    logfile.info("Subscribed to MQTT topic " + MQTT_TOPIC_OUT)

    mqtt_client.set_will(MQTT_TOPIC_IN)
    mqtt_client.client.loop_start()       


    #### CONFIGURE EDGWARE
    # Register edgware types
    result = registerEdgwareTypes(mqtt_client)
    assert result, "Error: Failed while registering Edgware component types"


    # Counters
    sqs_counter = 20
    mqtt_counter = 0
    while 1:
        # SQS Subloop - ~3s
        if sqs_counter == 30:
            sqs_counter = 0
            ## Get messages from SQS
            received_messages = sqs_queue.receive_messages(QueueUrl=sqs_queue.url, 
                                                           MessageAttributeNames=['All'], 
                                                           AttributeNames=['All'],
                                                           MaxNumberOfMessages=10)
            for message in received_messages:
                # Process incomming message
                result = processSQSInput(attributes=message.attributes, 
                                         message_attributes=message.message_attributes,
                                         body=message.body)

                 # Add to known platforms - expect tuple 
                if result is False:
                    logfile.error("Error: Failed to process message")
                else:
                    vehicle_id, platform_data = result

                    if vehicle_id not in known_platforms:
                        # Add entry and marked status
                        logfile.info(vehicle_id + " added to known platforms")                        
                        known_platforms[vehicle_id] = {}
                        known_platforms[vehicle_id]['data'] = platform_data
                        known_platforms[vehicle_id]['status'] = 'new'
                    else:
                        # Update entry
                        known_platforms[vehicle_id]['data'] = platform_data

                # Clear message from queue regardless of success/fail
                message.delete()


        # MQTT Subloop - ~4s
        if mqtt_counter == 40:
            mqtt_counter = 0

            for platform in known_platforms:
                # Register new platform and mark record
                if known_platforms[platform]['status'] == 'new':
                    result = registerNewPlatform(mqtt_client=mqtt_client, vehicle_id=platform)
                    assert result, "Error: Failed to register new platform " + platform

                    known_platforms[platform]['status'] = 'registered'

                # Update existing platforms
                else:
                    lat = known_platforms[platform]['data']['latitude']
                    long = known_platforms[platform]['data']['longitude']
                    alt = known_platforms[platform]['data']['altitude']
                      
                    updatePlatformPosition(mqtt_client=mqtt_client, 
                                           vehicle_id=platform,
                                           latitude=lat,
                                           longitude=long,
                                           altitude=alt)

      
        mqtt_counter += 1
        sqs_counter += 1
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

