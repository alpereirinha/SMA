class StationInfo:
    def __init__(self, plane_id, runway_dist, station_dist):
        self.plane_id = plane_id
        self.runway_distance = runway_dist
        self.station_distance = station_dist # 0 if already at station
        
    def __str__(self):
        return f'Plane {self.plane_id} to runway at distance {self.runway_distance}, and to station at distance {self.station_distance}.'
    
    def getPlaneId(self):
        return self.plane_id
    
    def getRunwayDistance(self):
        return self.runway_distance
    
    def getStationDistance(self):
        return self.station_distance
    
    def setPlaneId(self, plane_id):
        self.plane_id = plane_id

    def setRunwayDistance(self, runway_distance):
        self.runway_distance = runway_distance

    def setStationDistance(self, station_distance):
        self.station_distance = station_distance

    