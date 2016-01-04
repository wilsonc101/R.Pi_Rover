#!/usr/bin/python -B

def allStop(client=None):
    if client is None: return(False)

    try:
        instances = client.describe_instances()

        running_instances = []
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                # Running
                if 10 <= instance['State']['Code'] <= 19:
                    running_instances.append(instance['InstanceId'])

        response = client.stop_instances(InstanceIds=running_instances)
        return(response)

    except:
        return(False)



def allStart(client=None):
    if client is None: return(False)

    try:
        instances = client.describe_instances()

        stopped_instances = []
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                # Stopped
                if instance['State']['Code'] >= 80:
                    stopped_instances.append(instance['InstanceId'])

        response = client.start_instances(InstanceIds=stopped_instances)
        return(response)

    except:
        return(False)
