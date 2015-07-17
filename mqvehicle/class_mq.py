import json
import pika


class mqReader():
    def __init__(self, queue_host, queue_port, queue, callback, log=None):
    # Establish connection, queue and begin consuming
        self.log = log
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=queue_host,port=queue_port,connection_attempts=100,retry_delay=5))
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange=queue, type='fanout')

            self.result = self.channel.queue_declare(exclusive=True)
            self.dynamic_queue_name = self.result.method.queue
 
            self.channel.queue_bind(exchange=queue, queue=self.dynamic_queue_name)
            self.channel.basic_consume(callback, queue=self.dynamic_queue_name, no_ack=True)
            self.connected = True
            if self.log != None: self.log.info("Connected to reader queue.")

        except:
            if self.log != None: self.log.error("Failed to connect to reader queue.")
            self.connected = False


    def run(self):
        try:
            self.channel.start_consuming()
        except:
            if self.log != None:
                self.log.error("Connection to control queue server appears to have dropped.")
            else:
                print "ERROR: Connection to control queue server appears to have dropped."


class mqWriter():
    def __init__(self, queue_host, queue_port, queue, log=None):
    # Establish connection and queue for writing
        self.log = log
        try:
            self.queue = queue
            # Establish connection & queue
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(queue_host, queue_port, heartbeat_interval=1))
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange=queue, type='fanout')
            self.connected = True
            if self.log != None: self.log.info("Connected to writer queue.")

        except:
            if self.log != None: self.log.error("Failed to connect to writer queue.")
            self.connected = False
 

    def write(self, data):
        # Write JSON data to queue
        try:
            self.channel.basic_publish(exchange=self.queue, routing_key='', body=json.dumps(data))
            if self.log != None: self.log.debug("Writing data to vehicle queue")
            return(True)
        except:
            if self.log != None:
                self.log.warning("Connection to vehicle queue server appears to have dropped")
            else:
                print("Connection to vehicle queue server appears to have dropped")

            return(False)

