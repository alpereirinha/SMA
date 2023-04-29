from agents.controlTower import ControlTowerAgent
from agents.stationManager import StationManagerAgent
from agents.plane import PlaneAgent
from agents.dashboard import DashboardAgent
from classes.runway import Runway
from classes.station import Station
from spade import quit_spade
import time

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

    dashboard_jid = "dashboard" + XMPP_SERVER
    controlTower_jid = "controltower" + XMPP_SERVER
    stationManager_jid = "stationmanager" + XMPP_SERVER
    
    dashboard = DashboardAgent(dashboard_jid, PASSWORD)
    controlTower = ControlTowerAgent(controlTower_jid, PASSWORD)
    stationManager = StationManagerAgent(stationManager_jid, PASSWORD)
    
    res_controlTower = controlTower.start()
    res_controlTower.result()

    # Setup starting planes
    planes = []
    MAX = 5
    for i in range(1, MAX):
        plane_jid = "plane" + str(i) + XMPP_SERVER
        plane = PlaneAgent(plane_jid, PASSWORD)
        plane.set('company', 'Test Company')
        plane.set('origin', 'Test Origin')
        plane.set('destination', 'Test Destination')
        plane.set('controlTower_jid', controlTower_jid)

        if i%2:
            plane.set('type', SHIPPING)
        else:
            plane.set('type', LANDING)

        if i <= MAX/2:
            plane.set('state', FLYING)
        else:
            plane.set('state', LANDED)

        planes.append(plane)

    for p in planes:
        p.start()

    # Setup Runways/Stations
    # TODO

    while controlTower.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            controlTower.stop()
            for p in planes:
                p.stop()
            break

    quit_spade()