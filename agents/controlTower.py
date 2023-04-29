from spade.agent import Agent
from behaviours.rcvPlaneReq import rcvPlaneReqBehav

class ControlTowerAgent(Agent):

    async def setup(self):
        print('Starting Control Tower...')

        behav_rcvPlaneReq = rcvPlaneReqBehav()
        self.add_behaviour(behav_rcvPlaneReq)