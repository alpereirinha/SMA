from spade.agent import Agent

class RunwayAgent(Agent):

    async def setup(self):
        print('Starting Runway...')

        if self.get("landing_mode"):
            pass # add handlelanding
        if self.get("takeoff_mode"):
            pass # add handletakeoff