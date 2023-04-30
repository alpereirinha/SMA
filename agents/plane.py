from spade.agent import Agent
from behaviours.sendPlaneReq import sendPlaneReqBehav
from behaviours.listenPlaneUpdates import listenPlaneUpdatesBehav

class PlaneAgent(Agent):

    async def setup(self):
        print(f'Starting Plane...')

        behav_sendPlaneReq = sendPlaneReqBehav()
        behav_listenPlaneUpdates = listenPlaneUpdatesBehav()
        self.add_behaviour(behav_sendPlaneReq)
        self.add_behaviour(behav_listenPlaneUpdates)

