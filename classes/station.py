
class Station:
    def __init__(self, x, y, type, plane):
        self.coordinates = (x, y)
        self.type = type # SHIPPING / PASSENGERS
        self.plane = plane # '' / plane id

    def __str__(self):
        if self.plane:
            plane_str = f'holding {self.plane}.'
        else:
            plane_str = 'free.'
        
        return f'Station at {self.coordinates}, Type {self.type.name}. Currently ' + plane_str