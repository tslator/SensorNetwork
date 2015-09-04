class Sensor():
    def __init__(self, name, type, client, source):
        self.name = name
        self.type = type
        self.client = client
        self.source = source
        
    def Calibrate(self):
        print("Calibrating {0} ...".format(self.name))
        print("Complete!")
        pass
        
    def Announce(self):
        self.client.Connect()
        print("Announcing {0} ...".format(self.name))
        self.client.Publish("/sensor/config/{0}".format(self.name), "")
        print("Complete!")
        
    def Update(self):
        # Get the sensor value
        value = self.source.Next()
        #print(value)
        
        # Format the data for MQTT message
        value = str(value)
        
        # Publish the MQTT message
        self.client.Publish("/sensor/{0}/{1}".format(self.type, self.name), value)
        
class TemperatureSensor(Sensor):
    def __init__(self, *args, **kwargs):
        super().__init__(type = "temperature", *args, **kwargs)
        pass
        
        
class HumiditySensor(Sensor):
    def __init__(self, *args, **kwargs):
        super().__init__(type = "humidity", *args, **kwargs)
        pass
