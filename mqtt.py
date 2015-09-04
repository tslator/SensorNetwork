import paho.mqtt.client as mqtt

class MqttClient():
    def __init__(self, name, host, port, timeout):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.client = mqtt.Client(client_id=name)
        self.__subscriptions = []
        
    def __on_connect(self, client, userdata, flags, rc):
        print("Client {0} connected to broker with return code: {1}".format(client._client_id, str(rc)))
        for topic, callback in self.__subscriptions:
            self.client.subscribe(topic)
            
    def __on_message(self, client, userdata, msg):
        #print(client, userdata, msg)
        for topic, callback in self.__subscriptions:
            null, root, type, name = msg.topic.split('/')
            #print(root, type, name, msg.payload)
            callback(type, name, str(msg.payload))
        
    def Connect(self):
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.__on_message
        self.client.connect_async(host=self.host, port=self.port, keepalive=self.timeout)
        
    def Publish(self, topic, message):
        print("Publishing: {0} - {1}".format(topic, str(message)))
        self.client.publish(topic="{0}".format(topic), payload=str(message), qos=1)
        
    def Subscribe(self, topic, callback):
        self.__subscriptions.append( (topic, callback) )
        
    def Wait(self):
        self.client.loop_forever()
