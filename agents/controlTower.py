from spade.agent import Agent
from behaviours.rcvPlaneReq import rcvPlaneReqBehav
from behaviours.rcvStationInfo import rcvStationInfoBehav

class ControlTowerAgent(Agent):

    async def setup(self):
        print('Starting Control Tower...')

        behav_rcvPlaneReq = rcvPlaneReqBehav()
        behav_rcvStationInfo = rcvStationInfoBehav()
        self.add_behaviour(behav_rcvPlaneReq)
        self.add_behaviour(behav_rcvStationInfo)