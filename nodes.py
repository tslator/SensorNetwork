# There are two nodes in this system
#   1. Sensor node
#   2. Gateway node
#
# The sensor node acquires data from sensors, formats the data for publication, and publishes the data
# The gateway node subscribes to sensor messages, retreives sensor data and stores it in a repository
# Once stored, the data can be processed and displayed

import time
from mqtt import MqttClient
from datasrc import FileSource
from sensor import TemperatureSensor, HumiditySensor
from gateway import Gateway
from repo import Repository

KEEPALIVE = 60

def GetBrokerOptions(broker):
    host, port = broker.split(':')
    return (host, int(port))
    
# Sensor Node
def SensorNode(name, sensor_config_list, broker):
    
    # Create an MQTT client
    host, port = GetBrokerOptions(broker)
    mqtt_client = MqttClient(name, host, port, KEEPALIVE)
    
    # Create a list of sensors
    sensors = []
    for sensor in sensor_config_list:
        name, type, source, input = sensor
            
        if source == 'f':
            data_source = FileSource(input)
        if source == 'h':
            data_source = HwSource(input)
                
        if type == 't':
            sensors.append(TemperatureSensor(name = name, client = mqtt_client, source = data_source))
        if type == 'h':
            sensors.append(HumiditySensor(name = name, client = mqtt_client, source = data_source))
            
    for sensor in sensors:
        # Calibrate sensors
        sensor.Calibrate()
    
    for sensor in sensors:
        # Announce presence to MQTT Broker
        sensor.Announce()
    
    mqtt_client.client.loop_start()
    
    while True:
        # Periodically read data from sensor
        # Publish sensor message to MQTT Broker
        for sensor in sensors:
            sensor.Update()
        time.sleep(1)
    
# Gateway Node
def GatewayNode(name, broker):
    # Instantiate repository
    repo = Repository("output.csv", "csv")
    
    host, port = GetBrokerOptions(broker)
    mqtt_client = MqttClient(name, host, port, KEEPALIVE)
    
    gateway = Gateway(mqtt_client, repo)
    
    gateway.Connect()
    
    while True:
        # Wait for sensor message
        # Parse sensor message and store in repository
        gateway.Update()

        
if __name__ == "__main__":
    
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-r", "--role", action="store", type="string", dest="role", default="GATEWAY", help="Select the role of the node", metavar="SENSOR|GATEWAY")
    parser.add_option("-b", "--broker", action="store", type="string", dest="broker", default="localhost:1883", help="The MQTT Broker URI, e.g. localhost:1883", metavar="URL:PORT")
    
    (options, args) = parser.parse_args()

    node_name = input("Enter the name of this node:")
    
    if options.role == "SENSOR":
        num_sensors = int(input("Enter the number of supported sensors:"))
        sensor_list = []
        for i in range(num_sensors):
            sensor_name = input("Enter the name of the sensor:")
            sensor_type = input("Enter the sensor type (t : temperature, h : humidity)")
            sensor_source = input("Enter the data source for the sensor (f : file, h : hardware):")        
            if sensor_source == 'f':
                sensor_input = input("Enter the name of the data file:")
            else:
                sensor_input = int(input("Enter the input pin:"))
                
            sensor_list.append((sensor_name, sensor_type, sensor_source, sensor_input))
        

    print("Node Configuration Summary")
    print("\tNode Name:" + node_name)
    print("\tNode Role:" + options.role)
    
    if options.role == "SENSOR":
        print("\tNumber of Sensors:" + str(num_sensors))
        for entry in sensor_list:
            name, type, source, input = entry
            print("Sensor Name:" + name)
            print("Sensor Type:" + type)
            print("Sensor Source:" + source)
            print("Sensor Input:" + input)
            
            
    if options.role == "SENSOR":
        SensorNode(node_name, sensor_list, options.broker)
    if options.role == "GATEWAY":    
        GatewayNode(node_name, options.broker)
    
