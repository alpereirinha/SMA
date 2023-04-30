from spade.agent import Agent
from behaviours.controlTower.rcvPlaneReq import rcvPlaneReqBehav
from behaviours.controlTower.handleLanding import handleLandingBehav
from behaviours.controlTower.handleTakeoff import handleTakeoffBehav
from behaviours.controlTower.handleDelay import handleDelayBehav

class ControlTowerAgent(Agent):

    async def setup(self):
        print('Starting Control Tower...')

        behav_rcvPlaneReq = rcvPlaneReqBehav()
        behav_handleLanding = handleLandingBehav()
        behav_handleTakeoff = handleTakeoffBehav()
        behav_handleDelay = handleDelayBehav()

        self.add_behaviour(behav_rcvPlaneReq)
        self.add_behaviour(behav_handleLanding)
        self.add_behaviour(behav_handleTakeoff)
        self.add_behaviour(behav_handleDelay)