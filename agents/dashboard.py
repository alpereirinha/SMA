from spade.agent import Agent
from behaviours.dashboard.listenDashboard import listenDashboardBehav
import os

class DashboardAgent(Agent):

    async def setup(self):
        os.system('cls')
        print('+' + ('-'*78) + '+')
        print('|                          Plane Management Dashboard                          |')
        print('+' + ('-'*78) + '+')

        behav_listenDashboard = listenDashboardBehav()
        self.add_behaviour(behav_listenDashboard)