
class Runway:
    def __init__(self, x, y, action_type, plane):
        self.coordinates = (x, y)
        self.action_type = action_type # LANDING / TAKEOFF / MULTI
        self.plane = plane # '' / plane id

    def __str__(self):
        if self.plane:
            plane_str = f'holding {self.plane}.'
        else:
            plane_str = 'free.'
        
        return f'Runway at {self.coordinates}, Type {self.action_type.name}. Currently ' + plane_str