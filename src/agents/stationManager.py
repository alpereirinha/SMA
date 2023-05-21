from spade.agent import Agent
from behaviours.stationManager.listenStationInfoReq import listenStationInfoReqBehav
from behaviours.stationManager.listenStationUpdates import listenStationUpdatesBehav

class StationManagerAgent(Agent):

    async def setup(self):
        print('Starting Station Manager...')

        behav_listenStationInfoReq = listenStationInfoReqBehav()
        behav_listenStationUpdates = listenStationUpdatesBehav()
        self.add_behaviour(behav_listenStationInfoReq)
        self.add_behaviour(behav_listenStationUpdates)