from agents.dashboard import DashboardAgent
from agents.controlTower import ControlTowerAgent
from agents.stationManager import StationManagerAgent
from agents.plane import PlaneAgent
from classes.runway import *
from classes.station import *
from spade import quit_spade

XMPP_SERVER = ''
PASSWORD = ''

if __name__ == '__main__':

    dashboard = DashboardAgent("test1@sara-pc", "test1")

    #future = dashboard.start()
    #future.result()

    #quit_spade()