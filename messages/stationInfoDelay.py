
class StationInfoDelay:
    def __init__(self, plane_id, request_action, issue):
        self.plane_id = plane_id
        self.request_action = request_action # LANDING / TAKEOFF
        self.issue = issue
        
    def __str__(self):
        return f'Delayed {self.request_action.name} of {self.plane_id}. Issue: {self.issue}'
    
    def getPlaneId(self):
        return self.plane_id
    
    def getRequestAction(self):
        return self.request_action
    
    def getIssue(self):
        return self.issue
    
    def setPlaneId(self, plane_id):
        self.plane_id = plane_id

    def setRequestAction(self, request_action):
        self.request_action = request_action
    
    def setIssue(self, issue):
        self.issue = issue