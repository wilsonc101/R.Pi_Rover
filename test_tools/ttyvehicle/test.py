#!/usr/bin/python -B
import argparse

# Setup input arguments
arg_parser = argparse.ArgumentParser(description='Usage options for ttyvehicle')
arg_parser.add_argument('-c', '--configfile', help="Optional - configuration file path")
arg_parser.add_argument('-l', '--logfile', help="Optional - Log file path")

# Process input and generate dict
args = arg_parser.parse_args().__dict__

# Validate input
if args['configfile'] != None: 
    print args['configfile']
else:
    print "default config"


if args['logfile'] != None:
    print args['logfile']
else:
    print "default log"
