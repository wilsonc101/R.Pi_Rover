def launchBasicTiny(client, imageID, subnetID, securityGroups=[], region=None, count=1, public=True, keyname=None):
# Launch smallest instance in Free Tier (t2 Micro) using minimal inputs
    try:

        if keyname is None: keyname = region

        response = client.run_instances(ImageId=imageID,
                                        MinCount=1,
                                        MaxCount=int(count),
                                        KeyName=keyname,
                                        InstanceType='t2.micro',
                                        NetworkInterfaces=[{'SubnetId': subnetID, 
                                                            'Groups': securityGroups, 
                                                            'DeviceIndex': 0, 
                                                            'AssociatePublicIpAddress': public}])

        instance_list = [] 
        for instance in response['Instances']:
            instance_list.append(instance['InstanceId'])

        return(instance_list)

    except:
        return(False)



def getPublicIP(client=None, instanceID=None):
# Return public IP for single instance
    try:
        instance_list = [instanceID]

        instances = client.describe_instances(InstanceIds=instance_list)

        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                if instance['InstanceId'] == instanceID:
                    return(instance['PublicIpAddress'])

        return(False)
    except:
        return(False)
        
    

def getStatus(client=None, instanceID=None):
# Return status code as interger
    try:
        instance_list = [instanceID]

        instances = client.describe_instances(InstanceIds=instance_list)

        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                if instance['InstanceId'] == instanceID:
                    return(int(instance['State']['Code']))

        return(False)
    except:
        return(False)

