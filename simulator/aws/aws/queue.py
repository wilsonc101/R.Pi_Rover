def createQueue(client, name, message_retention_period=1800):
    try:
        # Fail if queue exists
        response = client.list_queues(QueueNamePrefix=name)
        if 'QueueUrls' in response and len(response['QueueUrls']) > 0: return False

        response = client.create_queue(QueueName=name,
                                       Attributes={'MessageRetentionPeriod':str(message_retention_period)})

        return response['QueueUrl']

    except:
        return False

