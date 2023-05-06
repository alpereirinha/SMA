from spade.agent import Agent
from behaviours.plane.sendPlaneReq import sendPlaneReqBehav
from behaviours.plane.listenPlaneUpdates import listenPlaneUpdatesBehav

class PlaneAgent(Agent):

    async def setup(self):
        behav_sendPlaneReq = sendPlaneReqBehav()
        behav_listenPlaneUpdates = listenPlaneUpdatesBehav()
        self.add_behaviour(behav_sendPlaneReq)
        self.add_behaviour(behav_listenPlaneUpdates)