from spade.agent import Agent
from classes.runway import *
from classes.station import *

class StationManagerAgent(Agent):

    runways = []
    stations = []

    async def setup(self):
        print('Starting Station Manager...')