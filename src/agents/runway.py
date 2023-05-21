from spade.agent import Agent
from behaviours.runway.handleLanding import handleLandingBehav
from behaviours.runway.handleTakeoff import handleTakeoffBehav

class RunwayAgent(Agent):

    async def setup(self):
        if self.get("landing_mode"):
            behav_handleLanding = handleLandingBehav()
            self.add_behaviour(behav_handleLanding)
        
        if self.get("takeoff_mode"):
            behav_handleTakeoff = handleTakeoffBehav()
            self.add_behaviour(behav_handleTakeoff)