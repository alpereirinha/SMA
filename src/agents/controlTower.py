from spade.agent import Agent
from behaviours.controlTower.listenPlanes import listenPlanesBehav
from behaviours.controlTower.processQueueLanding import processQueueLandingBehav
from behaviours.controlTower.processQueueTakeoff import processQueueTakeoffBehav
from behaviours.controlTower.processQueueMulti import processQueueMultiBehav
from behaviours.controlTower.listenStationResponse import listenStationResponseBehav
from behaviours.controlTower.listenRunways import listenRunwaysBehav

class ControlTowerAgent(Agent):

    landing_queue = []
    takeoff_queue = []
    multi_queue = []

    async def setup(self):
        print('Starting Control Tower...')

        behav_listenPlanes = listenPlanesBehav()
        behav_listenStationResponse = listenStationResponseBehav()
        behav_listenRunways = listenRunwaysBehav()
        self.add_behaviour(behav_listenPlanes)
        self.add_behaviour(behav_listenStationResponse)
        self.add_behaviour(behav_listenRunways)

        if self.get("multi_mode"):
            behav_processQueueMulti = processQueueMultiBehav()
            self.add_behaviour(behav_processQueueMulti)
        else:
            behav_processQueueLanding = processQueueLandingBehav()
            behav_processQueueTakeoff = processQueueTakeoffBehav()
            self.add_behaviour(behav_processQueueLanding)
            self.add_behaviour(behav_processQueueTakeoff)