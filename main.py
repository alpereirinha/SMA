from agents.controlTower import ControlTowerAgent
from agents.stationManager import StationManagerAgent
from agents.plane import PlaneAgent
from agents.dashboard import DashboardAgent
from classes.runway import Runway
from classes.station import Station
from classes.planeInfo import PlaneInfo
from spade import quit_spade

## Server Setup
XMPP_SERVER = '@sara-pc'
PASSWORD = '1234'

## Plane/Station Types
SHIPPING = 0
PASSENGERS = 1

## Runway Types
LANDING = 0
TAKEOFF = 1
MULTI = 2

## Plane States
FLYING = 0
LANDED = 1

## Station/Runway States
FREE = 0
OCCUPIED = 1

if __name__ == '__main__':

    controlTower_jid = "user1" + XMPP_SERVER
    stationManager_jid = "user2" + XMPP_SERVER
    plane_jid = "user3" + XMPP_SERVER
    dashboard_jid = "user4" + XMPP_SERVER

    controlTower = ControlTowerAgent(controlTower_jid, PASSWORD)
    stationManager = StationManagerAgent(stationManager_jid, PASSWORD)
    plane = PlaneAgent(plane_jid, PASSWORD)
    dashboard = DashboardAgent(dashboard_jid, PASSWORD)

    # needs container

    # Starting Planes
    #starting_planes = {}
    #starting_planes[1] = PlaneInfo('Test Company', 'Origin', 'Destination', SHIPPING, FLYING)
    #starting_planes[2] = PlaneInfo('Test Company', 'Origin', 'Destination', PASSENGERS, FLYING)
    #starting_planes[3] = PlaneInfo('Test Company', 'Origin', 'Destination', SHIPPING, LANDED)
    #starting_planes[4] = PlaneInfo('Test Company', 'Origin', 'Destination', PASSENGERS, LANDED)
    #planes.set('planes', starting_planes)

    # Setup Runways/Stations


    #future = controlTower.start()
    #future.result()

    #quit_spade()