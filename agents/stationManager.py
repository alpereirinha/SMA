from spade.agent import Agent
from behaviours.handleStationInfoReq import handleStationInfoReqBehav

class StationManagerAgent(Agent):

    async def setup(self):
        print('Starting Station Manager...')

        behav_handleStationInfoReq = handleStationInfoReqBehav()
        self.add_behaviour(behav_handleStationInfoReq)