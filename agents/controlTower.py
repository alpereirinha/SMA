from spade.agent import Agent
from behaviours.controlTower.listenPlaneReq import listenPlaneReqBehav
from behaviours.controlTower.processQueues import processQueuesBehav
from behaviours.controlTower.processQueueMulti import processQueueMultiBehav
from behaviours.controlTower.listenStationInfo import listenStationInfoBehav
from behaviours.controlTower.listenRunwayInfo import listenRunwayInfoBehav

class ControlTowerAgent(Agent):

    landing_queue = []
    takeoff_queue = []
    multi_queue = []

    async def setup(self):
        print('Starting Control Tower...')

        behav_listenPlaneReq = listenPlaneReqBehav()
        behav_listenStationInfo = listenStationInfoBehav()
        behav_listenRunwayInfo = listenRunwayInfoBehav()
        self.add_behaviour(behav_listenPlaneReq)
        self.add_behaviour(behav_listenStationInfo)
        self.add_behaviour(behav_listenRunwayInfo)

        if self.get("multi_mode"):
            behav_processQueueMulti = processQueueMultiBehav()
            self.add_behaviour(behav_processQueueMulti)
        else:
            behav_processQueues = processQueuesBehav()
            self.add_behaviour(behav_processQueues)