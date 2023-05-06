from spade.agent import Agent
from behaviours.controlTower.rcvPlaneReq import rcvPlaneReqBehav
from behaviours.controlTower.processPlaneReq import processPlaneReqBehav
from behaviours.controlTower.handleLanding import handleLandingBehav
from behaviours.controlTower.handleTakeoff import handleTakeoffBehav

class ControlTowerAgent(Agent):

    async def setup(self):
        print('Starting Control Tower...')

        behav_rcvPlaneReq = rcvPlaneReqBehav()
        behav_processPlaneReq = processPlaneReqBehav()
        behav_handleLanding = handleLandingBehav()
        behav_handleTakeoff = handleTakeoffBehav()

        self.add_behaviour(behav_rcvPlaneReq)
        self.add_behaviour(behav_processPlaneReq)
        self.add_behaviour(behav_handleLanding)
        self.add_behaviour(behav_handleTakeoff)