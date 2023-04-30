
class Station:
    def __init__(self, x, y, type, state, plane):
        self.coordinates = (x, y)
        self.type = type # SHIPPING / PASSENGERS
        self.state = state # FREE / OCCUPIED

    def __str__(self):
        return f'Station {self.id} at {self.coordinates}, Type {self.type}. Currently {self.state}.'