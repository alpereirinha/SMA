
#SHIPPING = 0
#PASSENGERS = 1

#LANDING = 0
#TAKEOFF = 1

class PlaneRequest:
    def __init__(self, plane_id, plane_type, request_type):
        self.plane_id = plane_id
        self.plane_type = plane_type
        self.request_type = request_type

    def __str__(self):
        return f'Request for {self.request_type}: Plane {self.plane_id}, Type {self.plane_type}.'
    
    #TODO