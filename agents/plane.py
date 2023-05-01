from spade.agent import Agent
from behaviours.plane.sendPlaneReq import sendPlaneReqBehav
from behaviours.plane.listenPlaneUpdates import listenPlaneUpdatesBehav
from behaviours.plane.listenPlaneDelays import listenPlaneDelaysBehav

class PlaneAgent(Agent):

    async def setup(self):
        behav_sendPlaneReq = sendPlaneReqBehav()
        behav_listenPlaneUpdates = listenPlaneUpdatesBehav()
        behav_listenPlaneDelays = listenPlaneDelaysBehav()

        self.add_behaviour(behav_sendPlaneReq)
        self.add_behaviour(behav_listenPlaneUpdates)
        self.add_behaviour(behav_listenPlaneDelays)

