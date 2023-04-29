
class Station:
    def __init__(self, x, y, type, state, plane):
        self.x = x
        self.y = y
        self.type = type # SHIPPING / PASSENGERS
        self.state = state # FREE / OCCUPIED
        self.landed_plane = plane

    def __str__(self):
        return f'Station {self.id} at ({self.x}, {self.y}), Type {self.type}. Currently {self.state}.'