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

## Server Info
XMPP_SERVER = '@sara-pc'
PASSWORD = '1234'

## Plane Options
MAX_PLANES = 4
companies = ['TAP', 'RyanAir', 'Delta', 'AirFrance']
locations = ['Lisbon', 'Madrid', 'Paris', 'London', 'Dublin', 'Berlin']

if __name__ == '__main__':

    dashboard_jid = "dashboard" + XMPP_SERVER
    controlTower_jid = "controltower" + XMPP_SERVER
    stationManager_jid = "stationmanager" + XMPP_SERVER
    
    dashboard = DashboardAgent(dashboard_jid, PASSWORD)
    controlTower = ControlTowerAgent(controlTower_jid, PASSWORD)
    stationManager = StationManagerAgent(stationManager_jid, PASSWORD)
    
    # Setup and start Control Tower
    controlTower.set('stationManager_jid', stationManager_jid)
    controlTower.set('dashboard_jid', dashboard_jid)
    res_controlTower = controlTower.start()
    res_controlTower.result()

    # Setup Runways
    runways = {}
    runways[(50, 50)] = Runway(Action.LANDING, '')
    runways[(0, 0)] = Runway(Action.TAKEOFF, '')
    stationManager.set("runways", runways)

    # Setup Stations
    stations = {}
    stations[(10, 10)] = Station(PlaneType.PASSENGERS, '')
    stations[(20, 20)] = Station(PlaneType.PASSENGERS, '')
    stations[(30, 30)] = Station(PlaneType.SHIPPING, '')
    stations[(15, 15)] = Station(PlaneType.SHIPPING, '')
    stations[(25, 25)] = Station(PlaneType.PASSENGERS, 'plane' + str(MAX_PLANES-1) + XMPP_SERVER)
    stations[(35, 35)] = Station(PlaneType.SHIPPING, 'plane' + str(MAX_PLANES) + XMPP_SERVER)
    stationManager.set("stations", stations)

    # Start Station Manager
    res_stationManager = stationManager.start()
    res_stationManager.result()

    # Start Dashboard
    res_dashboard = dashboard.start()
    res_dashboard.result()

    # Setup and start planes
    planes = []
    for i in range(1, MAX_PLANES+1):
        plane_jid = "plane" + str(i) + XMPP_SERVER
        plane = PlaneAgent(plane_jid, PASSWORD)

        locs = random.sample(locations, 2)
        plane.set('company', random.choice(companies))
        plane.set('origin', locs[0])
        plane.set('destination', locs[1])
        plane.set('controlTower_jid', controlTower_jid)

        if i%2:
            plane.set('type', PlaneType.SHIPPING)
        else:
            plane.set('type', PlaneType.PASSENGERS)

        if i <= (MAX_PLANES+1)/2:
            plane.set('state', PlaneState.FLYING)
        else:
            plane.set('state', PlaneState.LANDED)

        plane.start()
        planes.append(plane)

    # Run
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
    
    print('Agents stopped.')
    quit_spade()