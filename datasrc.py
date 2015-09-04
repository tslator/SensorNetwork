class DataSource():
    def __init__(self):
        # Can we make this a generator?
        pass
        
    def Next(self):
        pass
        
class FileSource(DataSource):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.fh = None
    
        # Check if we have opened the file
        if self.fh is None:
            try:
                self.fh = open(self.filename)
            except IOError:
                pass
        
    def Next(self):
        value = self.fh.readline().strip()
        if not value:
            self.fh.seek(0,0)
            value = self.fh.readline().strip()
        return value
                
class HwSource(DataSource):
    def __init__(self, input):
        pass
        
    def Next(self):
        pass
