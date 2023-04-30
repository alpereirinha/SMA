class StationInfo:
    def __init__(self, plane_id, request_action, runway_dist, station_dist):
        self.plane_id = plane_id
        self.request_action = request_action # LANDING / TAKEOFF
        self.runway_distance = runway_dist
        self.station_distance = station_dist # 0 if already at station
        
    def __str__(self):
        return f'{self.request_action.name} Approved: {self.plane_id} to runway at distance {self.runway_distance} and to station at distance {self.station_distance}.'
    
    def getPlaneId(self):
        return self.plane_id
    
    def getRequestAction(self):
        return self.request_action
    
    def getRunwayDistance(self):
        return self.runway_distance
    
    def getStationDistance(self):
        return self.station_distance
    
    def setPlaneId(self, plane_id):
        self.plane_id = plane_id

    def setRequestAction(self, request_action):
        self.request_action = request_action

    def setRunwayDistance(self, runway_distance):
        self.runway_distance = runway_distance

    def setStationDistance(self, station_distance):
        self.station_distance = station_distance

    