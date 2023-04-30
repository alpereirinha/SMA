from classes.enums import Action

class StationInfo:
    def __init__(self, plane_id, request_action, dist):
        self.plane_id = plane_id
        self.request_action = request_action # LANDING / TAKEOFF
        self.distance = dist # distance to station/runway
        
    def __str__(self):
        if self.distance > 0:
            if self.request_action == Action.LANDING:
                location = 'station'
            else:
                location = 'runway'

            str = f'{self.request_action.name} Approved: {self.plane_id} to {location} at distance {self.distance}.'
        
        else:
            str = f'Delayed {self.request_action.name} of {self.plane_id}.'
        
        return str
    
    def getPlaneId(self):
        return self.plane_id
    
    def getRequestAction(self):
        return self.request_action
    
    def getDistance(self):
        return self.distance
    
    def setPlaneId(self, plane_id):
        self.plane_id = plane_id

    def setRequestAction(self, request_action):
        self.request_action = request_action

    def setDistance(self, distance):
        self.distance = distance
    