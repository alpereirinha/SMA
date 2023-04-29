from spade.agent import Agent
from behaviours.reqLanding import reqLandingBehav
from behaviours.reqTakeoff import reqTakeoffBehav

SHIPPING = 0
PASSENGERS = 1

FLYING = 0
LANDED = 1

class PlaneAgent(Agent):

    id = 0
    company = ''
    origin = ''
    destination = ''
    type = SHIPPING
    state = FLYING

    async def setup(self):
        print('Starting Plane...')

        if self.state == FLYING:
            behav_reqLanding = reqLandingBehav()
            self.add_behaviour(behav_reqLanding)

        elif self.state == LANDED:
            behav_reqTakeoff = reqTakeoffBehav()
            self.add_behaviour(behav_reqTakeoff)

        # receiver confirmation...

        
        