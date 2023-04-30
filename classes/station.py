
class Station:
    def __init__(self, type, plane):
        self.type = type # SHIPPING / PASSENGERS
        self.plane = plane # '' / plane id
    
    def setType(self, type):
        self.type = type

    def setPlane(self, plane):
        self.plane = plane