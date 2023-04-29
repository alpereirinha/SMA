from spade.agent import Agent
from classes.runway import Runway
from classes.station import Station

LANDING = 0
TAKEOFF = 1
MULTI = 2

SHIPPING = 0
PASSENGERS = 1

FREE = 0
OCCUPIED = 1

class StationManagerAgent(Agent):

    runways = []
    stations = []

    async def setup(self):
        print('Starting Station Manager...')