from agents.controlTower import ControlTowerAgent
from agents.runway import RunwayAgent
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
STARTING_PLANES = 4
companies = ['TAP', 'RyanAir', 'Delta', 'AirFrance']
locations = ['Lisbon', 'Madrid', 'Paris', 'London', 'Dublin', 'Berlin']

## Station Default Options
STATIONS = 6

## Runway Default Options
RUNWAYS = 2
MULTI_RUNWAY = False

# Run Agents
def run():
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
    controlTower.set('max_landing_queue', STATIONS - math.ceil(STARTING_PLANES/2))
    controlTower.set('multi_mode', MULTI_RUNWAY)
    res_controlTower = controlTower.start()
    res_controlTower.result()

    # Prepare Runways / Setup and Start Runways
    runway_agents = []
    runways = {}
    for i in range(RUNWAYS):
        rw_jid = "runway" + str(i+1) + XMPP_SERVER
        rw = RunwayAgent(rw_jid, PASSWORD)
        rw.set('controlTower_jid', controlTower_jid)

        if MULTI_RUNWAY:
            rw.set("landing_mode", True)
            rw.set("takeoff_mode", True)
            runways[(0, 10*i)] = Runway(rw_jid, Action.MULTI, '')
        else:
            if i < RUNWAYS/2:
                rw.set("landing_mode", True)
                rw.set("takeoff_mode", False)
                runways[(0, 10*i)] = Runway(rw_jid, Action.LANDING, '')
            else:
                rw.set("landing_mode", False)
                rw.set("takeoff_mode", True)
                runways[(50, 10*i)] = Runway(rw_jid, Action.TAKEOFF, '')

        rw.start()
        runway_agents.append(rw)

    # Coordinates options for stations
    coords_x = random.sample(range(10, 40), STATIONS)
    coords_y = random.sample(range(10, 40), STATIONS)
    coords = list(zip(coords_x, coords_y))

    # Prepare Stations
    stations = {}
    for i in range(STATIONS):
        if i%2:
            planetype = PlaneType.SHIPPING
        else:
            planetype = PlaneType.PASSENGERS

        if i < STARTING_PLANES/2:
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
    i = 0
    while controlTower.is_alive():

        # Wait 10 seconds to add a new plane after starting batch
        if i >= STARTING_PLANES:
            try:
                time.sleep(10)
            except KeyboardInterrupt:
                controlTower.stop()
                stationManager.stop()
                dashboard.stop()
                for r in runway_agents:
                    r.stop()
                for p in plane_agents:
                    p.stop()
                break

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

        if i < STARTING_PLANES/2:
            plane.set('state', PlaneState.LANDED)
            plane.set('coordinates', coords[i])
        else:
            plane.set('state', PlaneState.FLYING)
            plane.set('coordinates', (random.randint(60,100), random.randint(60,100)) )

        plane.start()
        plane_agents.append(plane)
        i += 1
    
    print('Agents stopped.')
    quit_spade()


# Setup Command Line Options
if __name__ == '__main__':
    error = ''
    try:
        args, vals = getopt.getopt(sys.argv[1:], "hp:s:r:m", ["help", "planes", "stations", "runways", "multirunway"])
        for a, v in args:
            
            if a in ("-h", "--help"):
                print('\n\n*** Options ***\n')
                print('-h, --help : Show options')
                print('-p, --planes [number of planes] : Set number of initial planes. They will be split between landing/taking off, and passengers/shipping.')
                print('-s, --stations [number of stations] : Set number of stations. They will be split between passengers/shipping, and automatically filled with the already landed planes.')
                print('-r, --runways [number of runways] : Set number of runways. They will be split between for landing/takeoff unless multiuse mode is selected.')
                print('-m, --multirunway : Multiuse Mode. All runways can handle both landings and takeoffs.')
                error = '\n'
            
            elif a in ("-p", "--planes"):
                if v.isnumeric() and int(v) > 0:
                    STARTING_PLANES = int(v)
                else:
                    error = '[Error] Invalid number of planes.'
           
            elif a in ("-s", "--stations"):
                if v.isnumeric() and int(v) > 1:
                    STATIONS = int(v)
                elif int(v) == 1:
                    error = '[Error] No stations for shipping planes. Set larger number of stations.'
                else:
                    error = '[Error] Invalid number of stations.'
            
            elif a in ("-r", "--runways"):
                if v.isnumeric() and int(v) > 0:
                    RUNWAYS = int(v)
                else:
                    error = '[Error] Invalid number of runways.'
            
            elif a in ("-m", "--multirunway"):
                MULTI_RUNWAY = True
    
    except getopt.error as err:
        print(str(err))
        
    if error:
        print(error)
    elif STARTING_PLANES/2 > STATIONS:
        print('[Error] Not enough stations for number of landed planes.')
    elif RUNWAYS < 2 and not MULTI_RUNWAY:
        print('[Error] No takeoff runway. Set larger number of runways or use multiuses mode.')
    else:
        run()