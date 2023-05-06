from agents.controlTower import ControlTowerAgent
from agents.stationManager import StationManagerAgent
from agents.plane import PlaneAgent
from agents.dashboard import DashboardAgent
from classes.runway import Runway
from classes.station import Station
from classes.enums import *
from spade import quit_spade
import sys, getopt, time, random, math

## Server Info
XMPP_SERVER = '@sara-pc'
PASSWORD = '1234'

## Plane Default Options
MAX_PLANES = 4
companies = ['TAP', 'RyanAir', 'Delta', 'AirFrance']
locations = ['Lisbon', 'Madrid', 'Paris', 'London', 'Dublin', 'Berlin']

## Station Default Options
MAX_STATIONS = 6

## Runway Default Options
MULTI_RUNWAY = False

if __name__ == '__main__':

    # Use command line options to set number of planes and stations
    try:
        args, vals = getopt.getopt(sys.argv[1:], "hp:s:m", ["help", "planes", "stations", "multirunway"])
        for a, v in args:
            if a in ("-h", "--help"):
                print('\n*** Options ***\n')
                print('-h, --help : Show options')
                print('-p, --planes [number of planes] : Set number of initial planes')
                print('-s, --stations [number of stations] : Set number of stations')
                print('-m, --multirunway : Use a single runway for both landing and takeoff requests\n')
                exit()
            elif a in ("-p", "--planes"):
                MAX_PLANES = int(v)
            elif a in ("-s", "--stations"):
                MAX_STATIONS = int(v)
            elif a in ("-m", "--multirunway"):
                MULTI_RUNWAY = True
    except getopt.error as err:
        print(str(err))

    # Set JIDs and Agents
    dashboard_jid = "dashboard" + XMPP_SERVER
    controlTower_jid = "controltower" + XMPP_SERVER
    stationManager_jid = "stationmanager" + XMPP_SERVER
    
    dashboard = DashboardAgent(dashboard_jid, PASSWORD)
    controlTower = ControlTowerAgent(controlTower_jid, PASSWORD)
    stationManager = StationManagerAgent(stationManager_jid, PASSWORD)
    
    # Setup and Start Control Tower
    controlTower.set('stationManager_jid', stationManager_jid)
    controlTower.set('dashboard_jid', dashboard_jid)
    controlTower.set('max_landing_queue', MAX_STATIONS - math.ceil(MAX_PLANES/2))
    controlTower.set('landing_queue', [])
    controlTower.set('takeoff_queue', [])
    res_controlTower = controlTower.start()
    res_controlTower.result()

    # Prepare Runways
    runways = {}
    if MULTI_RUNWAY:
        runways[(0, 0)] = Runway(Action.MULTI, '')
    else:
        runways[(50, 50)] = Runway(Action.LANDING, '')
        runways[(0, 0)] = Runway(Action.TAKEOFF, '')

    # Coordinates options for stations
    coords_x = random.sample(range(10, 40), MAX_STATIONS)
    coords_y = random.sample(range(10, 40), MAX_STATIONS)
    coords = list(zip(coords_x, coords_y))

    # Prepare Stations
    stations = {}
    for i in range(MAX_STATIONS):
        if i%2:
            planetype = PlaneType.SHIPPING
        else:
            planetype = PlaneType.PASSENGERS

        if i < MAX_PLANES/2 or i >= MAX_PLANES:
            planelanded = ''
        else:
            planelanded = "plane" + str(i+1) + XMPP_SERVER

        stations[coords[i]] = Station(planetype, planelanded)

    # Setup and Start Station Manager
    stationManager.set("runways", runways)
    stationManager.set("stations", stations)
    res_stationManager = stationManager.start()
    res_stationManager.result()

    # Start Dashboard
    res_dashboard = dashboard.start()
    res_dashboard.result()

    # Setup and Start planes
    planes = []
    for i in range(MAX_PLANES):
        plane_jid = "plane" + str(i+1) + XMPP_SERVER
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

        if i < MAX_PLANES/2:
            plane.set('state', PlaneState.FLYING)
            plane.set('coordinates', (random.randint(60,100), random.randint(60,100)) )
        else:
            plane.set('state', PlaneState.LANDED)
            plane.set('coordinates', coords[i])

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
