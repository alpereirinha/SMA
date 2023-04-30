from spade.agent import Agent
from behaviours.dashboard.listenDashboard import listenDashboardBehav

class DashboardAgent(Agent):

    async def setup(self):
        print('Starting Dashboard...')

        behav_listenDashboard = listenDashboardBehav()
        self.add_behaviour(behav_listenDashboard)