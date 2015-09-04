import datetime

class Data():
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def Format(self, type):
        if type == "csv":
            return "{0},{1},{2}".format(self.name, self.type, self.value)
    
class Temperature(Data):
    def __init__(self, name, value):
        super().__init__(name, value)
        self.type = "temperature"

class Humidity(Data):
    def __init__(self, name, value):
        super().__init__(name, value)
        self.type = "humidity"
        
class Repository():
    def __init__(self, output, type):
        self.output = output
        self.type = type
        
    def Save(self, data):
        #print("Save")
        #print(data)
        #print(data.Format("csv"))
        if data is None:
            return
        if self.type == "csv":
            with open(self.output, 'a') as fh:
                # Record should look like this: <date>,<time>,<node>,<type>,<value>
                dt = datetime.datetime.now()
                value = '{0},{1},{2}\n'.format("{:%m/%d/%Y}".format(dt), "{:%H:%M:%S}".format(dt), data.Format("csv"))
                print(value)
                fh.write(value)            
