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
MAX_RUNWAYS = 2
MULTI_RUNWAY = False

if __name__ == '__main__':

    # Use command line options to set number of planes and stations
    try:
        args, vals = getopt.getopt(sys.argv[1:], "hp:s:r:m", ["help", "planes", "stations", "runways", "multirunway"])
        for a, v in args:
            if a in ("-h", "--help"):
                print('\n*** Options ***\n')
                print('-h, --help : Show options')
                print('-p, --planes [number of planes] : Set number of initial planes. They will be split between landing/taking off, and passengers/shipping.')
                print('-s, --stations [number of stations] : Set number of stations. They will be split between passengers/shipping, and automatically filled with the already landed planes.')
                print('-r, --runways [number of runwayss] : Set number of runways. They will be split between for landing/takeoff.')
                print('-m, --multirunway : All runways can handle both landings and takeoffs.\n')
                exit()
            elif a in ("-p", "--planes"):
                MAX_PLANES = int(v)
            elif a in ("-s", "--stations"):
                MAX_STATIONS = int(v)
            elif a in ("-r", "--runways"):
                MAX_RUNWAYS = int(v)
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
    controlTower.set('multi_mode', MULTI_RUNWAY)
    res_controlTower = controlTower.start()
    res_controlTower.result()

    # Prepare Runways / Setup and Start Runways
    runway_agents = []
    runways = {}
    for i in range(MAX_RUNWAYS):
        rw_jid = "runwayhandler" + str(i+1) + XMPP_SERVER
        rw = PlaneAgent(rw_jid, PASSWORD)

        if MULTI_RUNWAY:
            rw.set("landing_mode", True)
            rw.set("takeoff_mode", True)
            runways[(0, 10*i)] = Runway(Action.MULTI, '')
        else:
            if i < MAX_RUNWAYS/2:
                rw.set("landing_mode", True)
                rw.set("takeoff_mode", False)
                runways[(0, 10*i)] = Runway(Action.LANDING, '')
            else:
                rw.set("landing_mode", False)
                rw.set("takeoff_mode", True)
                runways[(50, 10*i)] = Runway(Action.TAKEOFF, '')

        rw.start()
        runway_agents.append(rw)
            
    #if MULTI_RUNWAY:
    #    runways[(0, 0)] = Runway(Action.MULTI, '')
    #else:
    #    runways[(0, 0)] = Runway(Action.LANDING, '')
    #    runways[(50, 50)] = Runway(Action.TAKEOFF, '')

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
            planelanded = "plane" + str(i+1) + XMPP_SERVER
        else:
            planelanded = ''
        
        stations[coords[i]] = Station(planetype, planelanded)

    # Setup and Start Station Manager
    stationManager.set("runways", runways)
    stationManager.set("stations", stations)
    res_stationManager = stationManager.start()
    res_stationManager.result()

    # Start Dashboard
    res_dashboard = dashboard.start()
    res_dashboard.result()

    # Setup and Start Planes
    plane_agents = []
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
            plane.set('state', PlaneState.LANDED)
            plane.set('coordinates', coords[i])
        else:
            plane.set('state', PlaneState.FLYING)
            plane.set('coordinates', (random.randint(60,100), random.randint(60,100)) )

        plane.start()
        plane_agents.append(plane)

    # Run
    while controlTower.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            controlTower.stop()
            stationManager.stop()
            dashboard.stop()
            for r in runway_agents:
                r.stop()
            for p in plane_agents:
                p.stop()
            break
    
    print('Agents stopped.')
    quit_spade()