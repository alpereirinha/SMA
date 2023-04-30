from spade.agent import Agent
from behaviours.sendPlaneReq import sendPlaneReqBehav

SHIPPING = 0
PASSENGERS = 1

FLYING = 0
LANDED = 1

class PlaneAgent(Agent):

    async def setup(self):
        print(f'Starting Plane...')

        behav_sendPlaneReq = sendPlaneReqBehav()
        self.add_behaviour(behav_sendPlaneReq)

        
        