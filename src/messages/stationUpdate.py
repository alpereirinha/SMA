
class StationUpdate:
    def __init__(self, plane_id, coords):
        self.plane_id = plane_id
        self.coordinates = coords

    def getPlaneId(self):
        return self.plane_id
    
    def getCoordinates(self):
        return self.coordinates
    
    def setPlaneId(self, plane_id):
        self.plane_id = plane_id

    def setCoordinates(self, coordinates):
        self.coordinates = coordinates