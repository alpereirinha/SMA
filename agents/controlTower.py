from spade.agent import Agent
from behaviours.handlePlaneReq import handlePlaneReqBehav

class ControlTowerAgent(Agent):

    async def setup(self):
        print('Starting Control Tower...')

        behav_handlePlaneReq = handlePlaneReqBehav()
        self.add_behaviour(behav_handlePlaneReq)