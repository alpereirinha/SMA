
class Runway:
    def __init__(self, id, action_type, plane):
        self.id = id
        self.action_type = action_type # LANDING / TAKEOFF / MULTI
        self.plane = plane # '' / plane id
        
    def setId(self, id):
        self.id = id
    
    def setActionType(self, action_type):
        self.action_type = action_type

    def setPlane(self, plane):
        self.plane = plane