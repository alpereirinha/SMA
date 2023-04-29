
LANDING = 0
TAKEOFF = 1
MULTI = 2

FREE = 0
OCCUPIED = 1

class Runway:
    def __init__(self, id, x, y, type, state):
        self.id = id
        self.x = x
        self.y = y
        self.type = type #landing/takeoff/multi
        self.state = state #free/occupied

    def __str__(self):
        return f'Runway {self.id} at ({self.x}, {self.y}), Type {self.type}. Currently {self.state}.'