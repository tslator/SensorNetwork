from repo import Temperature, Humidity

class Gateway():
    def __init__(self, client, repository):
        self.client = client
        self.repo = repository
        
        self.client.Subscribe("/sensor/+/+", self.__callback)
        
    def __callback(self, type, name, value):
        data = None
        if type == "temperature":
            data = Temperature(name, value)
        if type == "humidity":
            data = Humidity(name, value)
        
        #print("__callback")
        #print(data)
        #print(data.Format("csv"))
        # Store into the repository
        self.repo.Save(data)

    def Connect(self):
        self.client.Connect()
        
    def Update(self):
        self.client.Wait()
        
