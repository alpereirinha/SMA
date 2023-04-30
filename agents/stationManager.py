from spade.agent import Agent
from behaviours.stationManager.rcvStationInfoReq import rcvStationInfoReqBehav
from behaviours.stationManager.listenStationUpdates import listenStationUpdatesBehav

class StationManagerAgent(Agent):

    async def setup(self):
        print('Starting Station Manager...')

        behav_rcvStationInfoReq = rcvStationInfoReqBehav()
        behav_listenStationUpdates = listenStationUpdatesBehav()
        self.add_behaviour(behav_rcvStationInfoReq)
        self.add_behaviour(behav_listenStationUpdates)