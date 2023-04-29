
class PlaneRequest:
    def __init__(self, plane_jid, plane_type, request_type):
        self.plane_jid = plane_jid
        self.plane_type = plane_type #SHIPPING/PASSENGERS
        self.request_type = request_type #LANDING/TAKEOFF

    def __str__(self):
        return f'Request for {self.request_type}: Plane {self.plane_id}, Type {self.plane_type}.'

    def getPlaneJid(self):
        return self.plane_jid
    
    def getPlaneType(self):
        return self.plane_type
    
    def getRequestType(self):
        return self.request_type
    
    def setPlaneJid(self, plane_jid):
        self.plane_jid = plane_jid

    def setPlaneType(self, plane_type):
        self.plane_type = plane_type

    def setRequestType(self, request_type):
        self.request_type = request_type
