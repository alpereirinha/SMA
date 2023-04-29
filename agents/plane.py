from spade.agent import Agent

SHIPPING = 0
PASSENGERS = 1

FLYING = 0
LANDED = 1

class PlaneAgent(Agent):

    id = 0
    company = ""
    origin = ""
    destination = ""
    type = SHIPPING
    state = FLYING

    async def setup(self):
        print('Starting Plane...')