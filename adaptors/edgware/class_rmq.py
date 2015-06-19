import pika
import json

class rmqClientReader():
    def __init__(self, host, port, log=None):
        self.log = log
        self.pipe = None
        try:
            # Establish connection to broker
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,port=port,
                                                      connection_attempts=100,retry_delay=5))
            self.channel = self.connection.channel()
 
            self.connected = True
            if self.log != None: self.log.info("Connected to broker.")

        except:
            if self.log != None: self.log.error("Failed to connect to reader queue.")
            self.connected = False

    
    def subscribe(self, exchange, topic):
        try:
            # Declare exchange, create local queue and  bind queue to exchange with routing key
            self.channel.exchange_declare(exchange=exchange, type='topic')

            self.result = self.channel.queue_declare(exclusive=True)
            self.dynamic_queue_name = self.result.method.queue

            self.channel.queue_bind(exchange=exchange, queue=self.dynamic_queue_name, routing_key=topic)

            self.channel.basic_consume(self.on_message, queue=self.dynamic_queue_name, no_ack=True)
            return(True)
 
        except:
            if self.log != None: self.log.error("Failed to subscribe to" + str(topic))
            return(False)
     

    def on_message(self, ch, method, properties, body):
        # On message, emit data to multiprocessing queue
        self.pipe.send(body)


    def run(self, pipe):
        try:
            # Set multiprocessing queue as class global and begin consuming
            self.pipe = pipe
            self.channel.start_consuming()
        except:
            if self.log != None:
                self.log.error("Connection to broker appears to have dropped.")
            else:
                print "ERROR: Connection to broker appears to have dropped."



class rmqClientWriter():
    def __init__(self, host, port, log=None):
        self.log = log
        try:
            # Establish connection to broker
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host,port=port,heartbeat_interval=1))
            self.channel = self.connection.channel()
            self.connected = True
            if self.log != None: self.log.info("Connected to broker.")

        except:
            if self.log != None: self.log.error("Failed to connect to reader queue.")
            self.connected = False

    

    def publish(self, exchange, topic, body):
        try:
            self.channel.exchange_declare(exchange=exchange, type='topic')
            self.channel.basic_publish(exchange=exchange, routing_key=topic, body=body)
            if self.log != None: self.log.debug("Writing data to topic exchange")
            print "HERE!!!"
            return(True)

        except:
            if self.log != None:
                self.log.warning("Failed to send message to topic " + str(topic))
            else:
                print("Failed to send message to topic " + str(topic))
            return(False)

