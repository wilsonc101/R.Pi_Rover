#!/usr/bin/python -B

import sys
import os
import ConfigParser
import argparse
import boto3
import json
import time

import core.logger as log
import aws.tenancy as tenancy
import aws.instance as instance
import ssh.execute as ssh


# Setup input arguments
arg_parser = argparse.ArgumentParser(description='Usage options for aws_init')
arg_parser.add_argument('-c', '--configfile', help="Optional - configuration file path")
arg_parser.add_argument('-l', '--logfile', help="Optional - Log file path")
arg_parser.add_argument('-j', '--jsonfile', help="Path to JSON template file")
arg_parser.add_argument('-s', '--scriptfile', help="Path to Bash script file executed on instances")

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


# Validate script file path
if args['scriptfile'] is not None:
    assert os.path.isfile(args['scriptfile']), "Error: Script file path is incorrect or file does not exist"
    scriptfilepath = args['scriptfile']

else:
    scriptfilepath = None
    logfile.warn("No script file specififed - nothing will be run on instances")


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

# Enumerate file content for regions
deployed_instances = {}
for region in json_data['regions']:
    # Connect to region
    try:
        ec2_client = session.client('ec2', region_name=region['region'])
        logfile.info("Connected to AWS EC2 region " + region['region'])
    except:
        logfile.error("Error: EC2 not available in " + region['region'])
        assert False, "Error: EC2 not available in " + region['region']


    # Import keypair
    key_query_response = ec2_client.describe_key_pairs(Filters=[{'Name':'key-name', 'Values':[SECURITY_KEYNAME]}])

    if len(key_query_response['KeyPairs']) == 0:
        with open(SECURITY_PUBLIC_KEY) as publickeyfile:
            public_key = publickeyfile.read()

        ec2_client.import_key_pair(KeyName=SECURITY_KEYNAME, PublicKeyMaterial=public_key)
        logfile.info("Imported key " + SECURITY_KEYNAME)
	else:
	    logfile.info("Key " + SECURITY_KEYNAME + " already stored")

    # Check for VPCs in region matching CIDR block
    vpc_query_response = ec2_client.describe_vpcs(Filters=[{'Name':'cidr', 'Values':[region['region_cidr_block']]}])

    if len(vpc_query_response['Vpcs']) == 0:
    # Create new VPC
        vpc_id = tenancy.createVPC(client=ec2_client, 
                                   cidr_block=region['region_cidr_block'],
                                   create_gateway=bool(region['allow_internet_access']),
                                   set_internet_route=bool(region['allow_internet_access']),
                                   set_default_firewall_rules=bool(region['enable_default_access_rules']))
        assert vpc_id, "Error: Failed to create VPC in region " + region['region']
        logfile.info("Created VPC " + vpc_id + " in " + region['region'])
 
        # Create subnets       
        for subnet in region['subnets']:
            response = tenancy.createSubnet(client=ec2_client, 
                                            vpc_id=vpc_id, cidr_block=subnet['cidr_block'],
                                            availability_zone=subnet['availability_zone'])
                                            
            assert response, "Error: Failed to create subnet"
            logfile.info("Created subnet " + subnet['cidr_block'] + " in VPC " + vpc_id)

    elif len(vpc_query_response['Vpcs']) == 1:
    # VPC already exists (do not modify) - check for subnets
        vpc_id = vpc_query_response['Vpcs'][0]['VpcId']
        logfile.warning("VPC " + vpc_id + " already exists in " + region['region'])
        
        for subnet in region['subnets']:
            subnet_query_response = ec2_client.describe_subnets(Filters=[{'Name':'cidrBlock', 'Values':[subnet['cidr_block']]},
                                                                         {'Name':'vpc-id', 'Values':[vpc_id]}])
            # Create subnet if not present
            if len(subnet_query_response['Subnets']) == 0:
                response = tenancy.createSubnet(client=ec2_client, vpc_id=vpc_id, cidr_block=subnet['cidr_block'], availability_zone=subnet['availability_zone'])
                assert response, "Error: Failed to create subnet"
                logfile.info("Created subnet " + subnet['cidr_block'] + " in VPC " + vpc_id)
    else:
        # Can't handle more than one VPC - doesn't make sense (yet)
        logfile.error("Error: Unusable number of VPCs in " + region['region'])
        assert False, "Error: Unusable number of VPCs in " + region['region']

    # Instantiate vehicles
    region_instances = {}
    for vehicles in region['vehicles']:
        availability_zone = vehicles['location']
        instance_count = vehicles['count']
        image = vehicles['image']

        # Get ID for default security group
        security_group_id = tenancy.getSecurityGroupIDfromName(client=ec2_client, groupname=AWS_DEFAULT_SECURITY_GROUP_NAME)
        assert security_group_id, "Error: Could not get security group for " + AWS_DEFAULT_SECURITY_GROUP_NAME

        subnet_id = tenancy.getSubnetIDfromZone(client=ec2_client, zone=availability_zone, vpc_id=vpc_id)
        assert subnet_id, "Error: Could not get subnet for location " + availability_zone

        # Deploy instance
        deploy_response = instance.launchBasicTiny(client=ec2_client,
                                                   imageID=image,
                                                   subnetID=subnet_id,
                                                   securityGroups=[security_group_id],
                                                   region=region['region'],
                                                   count=instance_count,
                                                   keyname=SECURITY_KEYNAME)
        assert deploy_response, "Error: Failed to deploy instance"
        
        ## Populate temp dict with instance id and zone
        for instanceID in deploy_response:
            region_instances[instanceID] = {'zone':availability_zone}
            logfile.info("Deployed instance " + instanceID + " in region " + region['region'] + ", zone " + availability_zone)

    ## Populate global dict
    for instanceID in region_instances:
        # Hold while status is pending 
        state_query_response = instance.getStatus(client=ec2_client, instanceID=instanceID)
        while state_query_response < 10:
            time.sleep(5)
            state_query_response = instance.getStatus(client=ec2_client, instanceID=instanceID)

        # Get instance public IP
        ip_query_response = instance.getPublicIP(client=ec2_client, instanceID=instanceID)
        assert ip_query_response, "Error: Failed to return public IP"

        # Add record to dict
        deployed_instances[instanceID] = {'ip_address': ip_query_response, 
                                        'region':region['region'], 
                                        'zone':region_instances[instanceID]['zone']}

logfile.info("Success: All configuration complete")
 

if scriptfilepath is not None:
    # Loop deployed instances and run vehicle sim
    for instanceID in deployed_instances:
        # Connect to region
        try:
            ec2_client = session.client('ec2', region_name=deployed_instances[instanceID]['region'])
            logfile.info("Connected to AWS EC2 region " + deployed_instances[instanceID]['region'])
        except:
            logfile.error("Error: EC2 not available in " + region['region'])
            assert False, "Error: EC2 not available in " + region['region']

        waiter = ec2_client.get_waiter('instance_status_ok')

        instance_id = instanceID
        instance_ip = deployed_instances[instanceID]['ip_address']

        # Wait for instance to be ready
        logfile.info("Waiting for " + instance_id + " to become ready")
        waiter.wait(InstanceIds=[instance_id])

        # Run SSH commands
        logfile.info("Executing " + scriptfilepath + " on " + instance_id)
        response = ssh.runRemoteScript(remotehost=instance_ip,
                                   scriptpath=scriptfilepath,
                                   username=AWS_IMAGE_USERNAME,
                                   keyfilepath=SECURITY_PRIVATE_KEY)
        assert response, "Error: Failed to execute SSH commands"

        script_errors, script_output = response

        if len(script_output) > 0:
            for line in script_output:
                if "vehicleID:" in line: deployed_instances[instanceID]['vehicle_id'] = line.split(":")[1].strip('\n')
        logfile.info(instance_id + " ready")


logfile.info("Success: All instances running")
print str(deployed_instances)
