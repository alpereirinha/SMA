
class Runway:
    def __init__(self, action_type, plane):
        self.action_type = action_type # LANDING / TAKEOFF / MULTI
        self.plane = plane # '' / plane id
    
    def setActionType(self, action_type):
        self.action_type = action_type

    def setPlane(self, plane):
        self.plane = plane