from spade.agent import Agent
from behaviours.sendPlaneReq import sendPlaneReqBehav

class PlaneAgent(Agent):

    async def setup(self):
        print(f'Starting Plane...')

        behav_sendPlaneReq = sendPlaneReqBehav()
        self.add_behaviour(behav_sendPlaneReq)

        
        