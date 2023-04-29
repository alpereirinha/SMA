from spade.agent import Agent
from behaviours.handlePlaneReq import handlePlaneReqBehav
from behaviours.handleStationReply import handleStationReplyBehav

class ControlTowerAgent(Agent):

    async def setup(self):
        print('Starting Control Tower...')

        behav_handlePlaneReq = handlePlaneReqBehav()
        behav_handleStationReply = handleStationReplyBehav()
        self.add_behaviour(behav_handlePlaneReq)
        self.add_behaviour(behav_handleStationReply)