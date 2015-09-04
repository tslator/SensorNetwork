Purpose: This project implements a simple node network containing a single gateway node and several sensor nodes.  Each sensor node can have one or more sensors attached (presently there is support for a virtual temperature sensor and humidity sensor).  The sensor node collects information from the sensors and publishes the data using MQTT to the gateway node.  The gateway node subscribes to the sensor node messages and stores the data into a CSV file.  There is a simple webserver which reads the CSV file and display the data in a HTML page.

Usage:
The main module nodes.py and it implements both the gateway and the node.  Command-line options determine whether the launch application as a gateway or node.

  Supported options:
    Usage: nodes.py [options]
    
    Options:
      -h, --help            show this help message and exit
      -r SENSOR|GATEWAY, --role=SENSOR|GATEWAY
                            Select the role of the node
      -b URL:PORT, --broker=URL:PORT
                            The MQTT Broker URI, e.g. localhost:1883

    How to start the Gateway node:
      On the Gatway node type:
        python nodes.py -r GATEWAY -b localhost:1883
        
      The application interactively askes for the Gateway nodes name.
        
    How to start the Sensor node:
      On each Sensor node type:
        python nodes.py -r SENSOR -b <ip addr>:1883
  
      In addition, the application will prompt for the number, type, and data source of the attached sensors, e.g.,
      
        Enter the name of this node:sn-01
        Enter the number of supported sensors:2
        Enter the name of the sensor:sn01-tem01
        Enter the sensor type (t : temperature, h : humidity)t
        Enter the data source for the sensor (f : file, h : hardware):f
        Enter the name of the data file:tmp_sensor.dat
        Enter the name of the sensor:sn01-hum01
        Enter the sensor type (t : temperature, h : humidity)h
        Enter the data source for the sensor (f : file, h : hardware):f
        Enter the name of the data file:hum_sensor.dat
        Node Configuration Summary
          Node Name:sn-01
          Node Role:SENSOR
          Number of Sensors:2

Raspberry Pi Setup:

Unfortunately, github won't allow the actual Raspberry Pi image to be uploaded (too big).  So, below is a brief summary of setup for the Raspberry Pi.
  
  * Raspbian Wheezy image (updated and upgraded)
  * Mosquitto
      * wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
      * sudo apt-key add mosquitto-repo.gpg.key
      * rm mosquitto-repo.gpg.key
      * cd /etc/apt/sources.list.d/
      * sudo wget http://repo.mosquitto.org/debian/mosquitto-repo.list
      * sudo apt-get update
      * sudo apt-get install mosquitto mosquitto-clients
  * Python 3
  * PIP (should already be installed from Python 3)
  * Mosquitto Python wrapper
      pip install paho-mqtt
