#!/usr/bin/python -B

import sys
import os
import ConfigParser
import argparse
import boto3
import json

import core.logger as log

import aws.iam as iam
import aws.queue as queue



# Setup input arguments
arg_parser = argparse.ArgumentParser(description='Usage options for aws_init')
arg_parser.add_argument('-c', '--configfile', help="Optional - configuration file path")
arg_parser.add_argument('-l', '--logfile', help="Optional - Log file path")
arg_parser.add_argument('-j', '--jsonfile', help="Path to JSON template file")

# Process input and generate dict
args = vars(arg_parser.parse_args())


# Validate input - Config file
if args['configfile'] is not None:
    configfilepath = args['configfile']
else:
    local_path = os.path.dirname(os.path.abspath(__file__))
    configfilepath = str(local_path) + '/config/aws.cfg'

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


# Validate JSON file path
if args['jsonfile'] is not None:
    assert os.path.isfile(args['jsonfile']), "Error: JSON file path is incorrect or file does not exist"
    jsonfilepath = args['jsonfile']
else:
    assert False, "Error: No JSON file specified"


# Validate config
try:
    AWS_KEY_ID = config.get('aws_security', 'aws_access_key_id')
    AWS_KEY = config.get('aws_security', 'aws_secret_access_key')

    AWS_DEFAULT_REGION = config.get('aws_defaults', 'region')

    AWS_DEFAULT_SECURITY_GROUP_NAME = config.get('aws_defaults', 'security_group_name')
    AWS_DEFAULT_IMAGE = config.get('aws_defaults', 'image')
    AWS_IMAGE_USERNAME = config.get('aws_defaults', 'image_username')

    SECURITY_KEYNAME = config.get('keypair', 'name')
    SECURITY_PUBLIC_KEY = config.get('keypair', 'public')
    SECURITY_PRIVATE_KEY = config.get('keypair', 'private')
    logfile.debug("Configuration file loaded")

except ConfigParser.NoSectionError as err:
    logfile.error("Error: " + str(err))
    raise SystemExit("Error: " + str(err))

except ConfigParser.NoOptionError as err:
    logfile.error("Error: " + str(err))
    raise SystemExit("Error: " + str(err))

except:
    raise SystemExit("FATAL: Unknown error - " + str(sys.exc_info()[0]))


#### Connect to AWS resources
try:
    session = boto3.session.Session(aws_access_key_id=AWS_KEY_ID,
                                    aws_secret_access_key=AWS_KEY,
                                    region_name=AWS_DEFAULT_REGION)
    logfile.info("Connected to AWS")

except:
    logfile.error("Error: Could not connect to AWS")
    assert False, "Error: Could not connect to AWS"


## Open JSON template file
with open(jsonfilepath) as json_template:
    json_data = json.load(json_template)


# Setup SQS user access
if bool(json_data['create_global_sqs_users']) is True:
    try:
        iam_client = session.client('iam')
        logfile.info("Connected to AWS IAM")
    except:
        logfile.error("Error: IAM not available")
        assert False, "Error: IAM not available"

    # Create policies
    response = iam.createDefaultSQSPolicies(client=iam_client)
    assert response, "Error: Could not create SQS IAM policies"
    logfile.info("Default SQS IAM policies created")

    # Create users (and attach policies)
    response = iam.createDefaultSQSUsers(client=iam_client, attach_policies=True)
    assert response, "Error: Could not create SQS users"
    logfile.info("Created default SQS users")

logfile.info("Success: SQS access configuration complete")

deployed_queues = {}
for region in json_data['regions']:
    # Connect to region
    # SQS
    try:
        sqs_client = session.client('sqs', region_name=region['region'])
        logfile.info("Connected to AWS SQS region " + region['region'])
    except:
        logfile.error("Error: SQS not available in " + region['region'])
        assert False, "Error: SQS not available in " + region['region']

    for new_queue in region['queues']:
        queue_url = queue.createQueue(client=sqs_client, 
                                      name=new_queue['name'], 
                                      message_retention_period=new_queue['retention_period'])

        assert queue_url, "Error: Could not create queue " + new_queue['name'] + " in region " + region['region']

        deployed_queues[new_queue['name']] = {'url': queue_url}
        logfile.info("Created queue " + new_queue['name'] + ", url: " + queue_url )

logfile.info("Success: SQS queue(s) deployed")
print str(deployed_queues)
