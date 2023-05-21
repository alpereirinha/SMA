
class StationInfo:
    def __init__(self, plane_id, request_action, runway_id, runway_coords, station_coords, dist):
        self.plane_id = plane_id
        self.request_action = request_action # LANDING / TAKEOFF
        self.runway_id = runway_id
        self.runway_coords = runway_coords
        self.station_coords = station_coords
        self.distance = dist # distance between station/runway
    
    def getPlaneId(self):
        return self.plane_id
    
    def getRequestAction(self):
        return self.request_action
    
    def getRunwayId(self):
        return self.runway_id
    
    def getRunwayCoords(self):
        return self.runway_coords
    
    def getStationCoords(self):
        return self.station_coords
    
    def getDistance(self):
        return self.distance
    
    def setPlaneId(self, plane_id):
        self.plane_id = plane_id

    def setRequestAction(self, request_action):
        self.request_action = request_action

    def setRunwayId(self, runway_id):
        self.runway_id = runway_id

    def setRunwayCoords(self, runway_coords):
        self.runway_coords = runway_coords

    def setStationCoords(self, station_coords):
        self.station_coords = station_coords

    def setDistance(self, distance):
        self.distance = distance
    