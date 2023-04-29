
class Runway:
    def __init__(self, x, y, type, state):
        self.x = x
        self.y = y
        self.type = type # LANDING / TAKEOFF / MULTI
        self.state = state # FREE / OCCUPIED

    def __str__(self):
        return f'Runway {self.id} at ({self.x}, {self.y}), Type {self.type}. Currently {self.state}.'