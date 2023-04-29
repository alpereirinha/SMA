
SHIPPING = 0
PASSENGERS = 1

FREE = 0
OCCUPIED = 1

class Station:
    def __init__(self, id, x, y, type, state):
        self.id = id
        self.x = x
        self.y = y
        self.type = type #shipping/passengers
        self.state = state #free/occupied

    def __str__(self):
        return f'Station {self.id} at ({self.x}, {self.y}), Type {self.type}. Currently {self.state}.'