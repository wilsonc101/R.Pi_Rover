import paho.mqtt.client as mqtt


class mqttClient():
    def __init__(self, host, port, pipe, client_id="paho", keepalive=60, log=None):
        self.pipe = pipe
        self.log = log
        self.id = client_id
 
        self.client = mqtt.Client(client_id=self.id, clean_session=True)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        try:
            self.client.connect(host, port, keepalive)
            self.client.loop()
            self.connected = True


        except:
            self.connected = False

    def on_connect(self, client, userdata, flags, rc):
        if self.log != None:
            self.log.info("MQTT Connection status:" + str(rc))
 
    def on_message(self, client, userdata, msg):
        self.pipe.send(str(msg.payload))


    def subscribe(self, topic, qos=0):
        try:
            self.client.subscribe(topic, qos)
            if self.log != None:
                self.log.info("Subscribed to " + topic)
            return True

        except:
            if self.log != None:
                self.log.error("Failed to subscribe to " + topic)
            return False


    def unsubscribe(self, topic):
        try:
            self.client.unsubscribe(topic)
            if self.log != None:
                self.log.info("Unsubscribed from " + topic)
            return True

        except:
            if self.log != None:
                self.log.error("Failed to unsubscribe from " + topic)
            return False


    def publish(self, topic, payload, qos=0):
        try:
            self.client.publish(topic, payload=payload, qos=qos)
            if self.log != None:
                self.log.debug("Published message: " + payload)
            return True

        except:
            if self.log != None:
                self.log.error("Failed to publish message to " + topic)
            return False


    def set_will(self, topic):
        payload = '{"op": "disconnect","client-id":' +  self.id + '}'
        self.client.will_set(topic, payload)


    def run(self):
        try:
            self.client.loop_start()

        except:
            if self.log != None:
                self.log.error("Failed to enter consumer loop")
