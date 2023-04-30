
class PlaneRequest:
    def __init__(self, plane_id, plane_type, request_action):
        self.plane_id = plane_id
        self.plane_type = plane_type # SHIPPING / PASSENGERS
        self.request_action = request_action # LANDING / TAKEOFF

    def __str__(self):
        return f'Request for {self.request_action.name}: {self.plane_id}, Type {self.plane_type.name}.'

    def getPlaneId(self):
        return self.plane_id
    
    def getPlaneType(self):
        return self.plane_type
    
    def getRequestAction(self):
        return self.request_action
    
    def setPlaneId(self, plane_id):
        self.plane_id = plane_id

    def setPlaneType(self, plane_type):
        self.plane_type = plane_type

    def setRequestAction(self, request_action):
        self.request_action = request_action
