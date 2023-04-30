from spade.agent import Agent
from behaviours.rcvStationInfoReq import rcvStationInfoReqBehav

class StationManagerAgent(Agent):

    async def setup(self):
        print('Starting Station Manager...')

        behav_rcvStationInfoReq = rcvStationInfoReqBehav()
        self.add_behaviour(behav_rcvStationInfoReq)