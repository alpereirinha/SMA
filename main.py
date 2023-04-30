from agents.controlTower import ControlTowerAgent
from agents.stationManager import StationManagerAgent
from agents.plane import PlaneAgent
from agents.dashboard import DashboardAgent
from classes.runway import Runway
from classes.station import Station
from classes.enums import *
from spade import quit_spade
import time
import random

## Server Setup
XMPP_SERVER = '@sara-pc'
PASSWORD = '1234'

if __name__ == '__main__':

    dashboard_jid = "dashboard" + XMPP_SERVER
    controlTower_jid = "controltower" + XMPP_SERVER
    stationManager_jid = "stationmanager" + XMPP_SERVER
    
    dashboard = DashboardAgent(dashboard_jid, PASSWORD)
    controlTower = ControlTowerAgent(controlTower_jid, PASSWORD)
    stationManager = StationManagerAgent(stationManager_jid, PASSWORD)
    
    controlTower.set('stationManager_jid', stationManager_jid)
    controlTower.set('dashboard_jid', dashboard_jid)
    res_controlTower = controlTower.start()
    res_controlTower.result()

    # Setup Runways/Stations
    runways = []
    stations = []
    
    runways.append(Runway(50, 50, Action.LANDING, ''))
    runways.append(Runway(0, 0, Action.TAKEOFF, ''))
    stationManager.set("runways", runways)

    stations.append(Station(random.randint(0, 50), random.randint(0, 50), PlaneType.PASSENGERS, ''))
    stations.append(Station(random.randint(0, 50), random.randint(0, 50), PlaneType.PASSENGERS, ''))
    stations.append(Station(random.randint(0, 50), random.randint(0, 50), PlaneType.SHIPPING, ''))
    stations.append(Station(random.randint(0, 50), random.randint(0, 50), PlaneType.SHIPPING, ''))
    stations.append(Station(random.randint(0, 50), random.randint(0, 50), PlaneType.PASSENGERS, 'plane3@sara-pc'))
    stations.append(Station(random.randint(0, 50), random.randint(0, 50), PlaneType.SHIPPING, 'plane4@sara-pc'))
    stationManager.set("stations", stations)

    res_stationManager = stationManager.start()
    res_stationManager.result()

    res_dashboard = dashboard.start()
    res_dashboard.result()

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
            plane.set('type', PlaneType.SHIPPING)
        else:
            plane.set('type', PlaneType.PASSENGERS)

        if i <= MAX/2:
            plane.set('state', PlaneState.FLYING)
        else:
            plane.set('state', PlaneState.LANDED)

        planes.append(plane)

    for p in planes:
        p.start()

    while controlTower.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            controlTower.stop()
            stationManager.stop()
            dashboard.stop()
            for p in planes:
                p.stop()
            break

    quit_spade()