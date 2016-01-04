# Default Rules
_outbound_rule_01 = {'RuleNumber':100, 
                     'Egress':True, 
                     'CidrBlock':'0.0.0.0/0', 
                     'Protocol':'-1', 
                     'RuleAction':'allow',
                     'Description':'OUT-All'}

_inbound_rule_01 = {'RuleNumber':10, 
                    'Egress':False, 
                    'CidrBlock':'<MY_IP_HERE>/32', 
                    'PortRange':{'To': 22, 'From': 22},
                    'Protocol':'6', 
                    'RuleAction':'allow',
                    'Description':'IN-SSH-MyAccess'}

_inbound_rule_02 = {'RuleNumber':20, 
                    'Egress':False, 
                    'CidrBlock':'<MY_IP_HERE>/32', 
                    'PortRange':{'To': 3389, 'From': 3389},
                    'Protocol':'6', 
                    'RuleAction':'allow',
                    'Description':'IN-RDP-MyAccess'}

_inbound_rule_03 = {'RuleNumber':200, 
                    'Egress':False, 
                    'CidrBlock':'0.0.0.0/0', 
                    'PortRange':{'To': 61000, 'From': 32768},
                    'Protocol':'6', 
                    'RuleAction':'allow',
                    'Description':'IN-Eph-All'}

_default_rules = [_inbound_rule_01, _inbound_rule_02, _inbound_rule_03, _outbound_rule_01]


def createVPC(client, cidr_block, tenancy="default", create_gateway=True, set_internet_route=True, set_default_firewall_rules=True):
# Creates VPC with optional internet connections/firewall rules
    try:
        # Basic check for CIDR notation - improve with Regex
        if "/" not in cidr_block: return(False)

        response = client.create_vpc(CidrBlock=cidr_block, InstanceTenancy=tenancy)

        vpc_id = response['Vpc']['VpcId']

        # Create gateway
        if create_gateway == True:
            response = client.create_internet_gateway()
            gateway_id = response['InternetGateway']['InternetGatewayId']
            client.attach_internet_gateway(InternetGatewayId=gateway_id, VpcId=vpc_id)

        # Set 0.0.0.0 route
        if set_internet_route == True:
            response = client.describe_route_tables(Filters=[{'Name':'vpc-id', 'Values':[vpc_id]}])
            for route_table in response['RouteTables']:
                if route_table['VpcId'] == vpc_id:
                    route_table_id = route_table['RouteTableId']

            client.create_route(RouteTableId=route_table_id, DestinationCidrBlock="0.0.0.0/0", GatewayId=gateway_id)

        # Add default firewall rules
        if set_default_firewall_rules == True:
            # Get new Network ACL ID
            response = client.describe_network_acls(Filters=[{'Name':'vpc-id', 'Values':[vpc_id]}])
            for network_acl in response['NetworkAcls']:
                if network_acl['VpcId'] == vpc_id:
                    network_acl_id = network_acl['NetworkAclId']

            for rule in _default_rules:
                if 'PortRange' in rule:
                    client.create_network_acl_entry(NetworkAclId=network_acl_id,
                                                RuleNumber=rule['RuleNumber'],
                                                Protocol=rule['Protocol'],
                                                RuleAction=rule['RuleAction'],
                                                Egress=bool(rule['Egress']),
                                                CidrBlock=rule['CidrBlock'],
                                                PortRange=rule['PortRange'])
                elif 'IcmpTypeCode' in rule:
                    client.create_network_acl_entry(NetworkAclId=network_acl_id,
                                                RuleNumber=rule['RuleNumber'],
                                                Protocol=rule['Protocol'],
                                                RuleAction=rule['RuleAction'],
                                                Egress=bool(rule['Egress']),
                                                CidrBlock=rule['CidrBlock'],
                                                IcmpTypeCode=rule['IcmpTypeCode'])

                else:
                    client.create_network_acl_entry(NetworkAclId=network_acl_id,
                                                RuleNumber=rule['RuleNumber'],
                                                Protocol=rule['Protocol'],
                                                RuleAction=rule['RuleAction'],
                                                Egress=bool(rule['Egress']),
                                                CidrBlock=rule['CidrBlock'])

                # Create matching security groups for inbound rules
                if rule['Egress'] == False and 'PortRange' in rule:
                    group_id = createSecurityGroup(client=client, vpc_id=vpc_id, groupname=rule['Description'])
                    if group_id != False:
                        client.authorize_security_group_ingress(GroupId=group_id, 
                                                                IpProtocol=rule['Protocol'],
                                                                FromPort=rule['PortRange']['From'],
                                                                ToPort=rule['PortRange']['To'],
                                                                CidrIp=rule['CidrBlock'])                                                    

            # Remove default inbound 'any:any' rule (100)
            client.delete_network_acl_entry(NetworkAclId=network_acl_id, RuleNumber=100, Egress=False)

        return(vpc_id)

    except:
        return(False)




def createSubnet(client, vpc_id, cidr_block, availability_zone=None):
# Creates subnet
    try:
        # Basic check for CIDR notation - improve with Regex
        if "/" not in cidr_block: return(False)

        if availability_zone is None or availability_zone == "Default" or availability_zone == "default":
            client.create_subnet(VpcId=vpc_id, CidrBlock=cidr_block)
        else:
            client.create_subnet(VpcId=vpc_id, CidrBlock=cidr_block, AvailabilityZone=availability_zone)

        return(True)

    except:
        return(False)
    

def createSecurityGroup(client, vpc_id, groupname, description=None):
# Creates security group
    try:
        if description is None: description = groupname

        response = client.create_security_group(GroupName=groupname, Description=description, VpcId=vpc_id)
        group_id = response['GroupId']

        return group_id

    except:
        return(False)



def getSecurityGroupIDfromName(client, groupname):
# Returns security group ID from name
    try:
        response = client.describe_security_groups(Filters=[{'Name':'group-name', 'Values':[groupname]}])

        for group in response['SecurityGroups']:
            if group['GroupName'] == groupname:
                return group['GroupId']

    except:
        return(False)


def getSubnetIDfromZone(client, zone, vpc_id):
# Returns subnet if from availability zone
    try:
        response = client.describe_subnets(Filters=[{'Name':'availabilityZone', 'Values':[zone]},
                                                    {'Name':'vpc-id', 'Values':[vpc_id]}])

        for subnet in response['Subnets']:
            if subnet['AvailabilityZone'] == zone:
                return subnet['SubnetId']

    except:
        return(False)


