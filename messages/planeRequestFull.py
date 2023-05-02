from messages.planeRequest import PlaneRequest

class PlaneRequestFull(PlaneRequest):
    def __init__(self, plane_id, plane_type, request_action, company, origin, destination):
        super().__init__(plane_id, plane_type, request_action)
        self.company = company
        self.origin = origin
        self.destination = destination

    def toPlaneRequest(self):
        return PlaneRequest(self.plane_id, self.plane_type, self.request_action)
    
    def getCompany(self):
        return self.company
    
    def getOrigin(self):
        return self.origin
    
    def getDestination(self):
        return self.destination
    
    def setCompany(self, company):
        self.company = company

    def setOrigin(self, origin):
        self.origin = origin

    def setDestination(self, destination):
        self.destination = destination