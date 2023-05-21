
class PlaneRequest:
    def __init__(self, plane_id, plane_type, plane_coords, request_action):
        self.plane_id = plane_id
        self.plane_type = plane_type # SHIPPING / PASSENGERS
        self.plane_coords = plane_coords # (x, y)
        self.request_action = request_action # LANDING / TAKEOFF

    def getPlaneId(self):
        return self.plane_id
    
    def getPlaneType(self):
        return self.plane_type
    
    def getPlaneCoords(self):
        return self.plane_coords
    
    def getRequestAction(self):
        return self.request_action
    
    def setPlaneId(self, plane_id):
        self.plane_id = plane_id

    def setPlaneType(self, plane_type):
        self.plane_type = plane_type

    def setPlaneCoords(self, plane_coords):
        self.plane_coords = plane_coords

    def setRequestAction(self, request_action):
        self.request_action = request_action
