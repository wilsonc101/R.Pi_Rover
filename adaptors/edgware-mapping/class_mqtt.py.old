import paho.mqtt.client as mqtt

class mqttClient():
    def __init__(self, host, port, pipe, client_id="paho", keepalive=60, log=None):
        self.pipe = pipe
        self.log = log
        self.id = client_id
        
        self.client = mqtt.Client(client_id=self.id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        try:
            self.client.connect(host, port, keepalive)
            self.client.loop()
            self.connected = True


        except:
            self.connected = False

    def on_connect(self, client, userdata, flags, rc):
            if self.log != None: self.log.info("MQTT Connection status:" + st(rc))
         
    def on_message(self, client, userdata, msg):
        self.pipe.send(str(msg.payload))


    def subscribe(self, topic, qos=0):
        try:
            self.client.subscribe(topic, qos)
            if self.log != None: self.log.info("Subscribed to " + topic)

        except:
            if self.log != None: self.log.error("Failed to subscribe to " + topic)


    def unsubscribe(self, topic):
        try:
            self.client.unsubscribe(topic)
            if self.log != None: self.log.info("Unsubscribed from " + topic)

        except:
            if self.log != None: self.log.error("Failed to unsubscribe from " + topic)
 

    def publish(self, topic, payload, qos=0):
         try:
             self.client.publish(topic, payload=payload, qos=qos)
             if self.log != None: self.log.debug("Published message: " + payload)

         except:
             if self.log != None: self.log.error("Failed to publish message to " + topic)
     

    def run(self):
        try:
            self.client.loop_start()

        except:
             if self.log != None: self.log.error("Failed to enter consumer loop")
 

