#!/usr/bin/python -B

import ConfigParser
import argparse
import sys
import os

import core.logger as log
import api.bulk_actions as bulk
import api.container as container
import api.image as image
import api.common as common

# Setup input arguments
arg_parser = argparse.ArgumentParser(description='Usage options for docker automation')
arg_parser.add_argument('-c', '--configfile', help="Optional - configuration file path")
arg_parser.add_argument('-l', '--logfile', help="Optional - Log file path")

# Process input and generate dict
args = vars(arg_parser.parse_args())


# Validate input - Config file
if args['configfile'] != None:
    configfilepath = args['configfile']
else:
    local_path = os.path.dirname(os.path.abspath(__file__))
    configfilepath = str(local_path) + '/config/docker.cfg'

# Get config
try:
    config = ConfigParser.ConfigParser()
    config.read(configfilepath)
except:
    raise SystemExit("FATAL: Unknown error - " + str(sys.exc_info()[0]))


# Validate input - Log file
if args['logfile'] != None:
    logfilepath = args['logfile']
else:
    logfilepath = config.get('logging', 'path')    

# Setup logging
try:
    LOGFILE = log.CreateLogger(toconsole=False,
                               tofile=True,
                               filepath=logfilepath,
                               level=config.get('logging', 'level'))
    assert LOGFILE, "Error: Failed to create log outputs"

except:
    raise SystemExit("FATAL: Unknown error - " + str(sys.exc_info()[0]))


# Get config elements
try:
    DOCKER_HOST = config.get('connection', 'host')
    DOCKER_HOST_PORT = config.get('connection', 'port')

except ConfigParser.NoSectionError as err:
    raise SystemExit("Error: " + str(err))

except ConfigParser.NoOptionError as err:
    raise SystemExit("Error: " + str(err))

except:
    raise SystemExit("FATAL: Unknown error - " + str(sys.exc_info()[0]))




