class StationInfo:
    def __init__(self, plane_jid, runway_dist, station_dist):
        self.plane_jid = plane_jid
        self.runway_distance = runway_dist
        self.station_distance = station_dist # 0 if already at station
        
    def __str__(self):
        return f'Plane {self.plane_jid} to runway at distance {self.runway_distance}, and to station at distance {self.station_distance}.'
    
    def getPlaneJid(self):
        return self.plane_jid
    
    def getRunwayDistance(self):
        return self.runway_distance
    
    def getStationDistance(self):
        return self.station_distance
    
    def setPlaneJid(self, plane_jid):
        self.plane_jid = plane_jid

    def setRunwayDistance(self, runway_distance):
        self.runway_distance = runway_distance

    def setStationDistance(self, station_distance):
        self.station_distance = station_distance

    