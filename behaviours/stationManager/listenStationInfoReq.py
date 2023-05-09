from spade.behaviour import CyclicBehaviour
from messages.stationInfo import StationInfo
from messages.requestDelay import RequestDelay
from classes.enums import *
import math
import jsonpickle

class listenStationInfoReqBehav(CyclicBehaviour):

    async def on_start(self):
        self.runways = self.get("runways")
        self.stations = self.get("stations")
    
    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            # Received valid request
            if performative == "request":
                msg_data = jsonpickle.decode(msg.body)
                req_action = msg_data.getRequestAction()
                plane_id = str(msg_data.getPlaneId())
                
                # Check runways
                available_runways = []
                for c, r in self.runways.items():
                    if (r.action_type == req_action or r.action_type == Action.MULTI) and not r.plane:
                        available_runways.append(c)

                # If runway available
                if len(available_runways) > 0 :

                    # Find closest runway to current coordinates
                    curr_coords = msg_data.getPlaneCoords()
                    closest_runway = get_closest(curr_coords, available_runways)
                    closest_runway_coords = closest_runway[0]
                    closest_runway_dist = closest_runway[1]
                    closest_runway_id = self.runways[closest_runway_coords].id

                    # If LANDING check for closest compatible station
                    if req_action == Action.LANDING:
                        plane_type = msg_data.getPlaneType()
                        available_stations = []

                        # Check for compatible free stations
                        for c, s in self.stations.items():
                            if s.type == plane_type and not s.plane:
                                available_stations.append(c)

                        # If station available
                        if len(available_stations) > 0 :
                            
                            # Find closest station to runway
                            closest_station = get_closest(closest_runway_coords, available_stations)
                            closest_station_coords = closest_station[0]
                            closest_station_dist = closest_station[1]

                            # Notify Control Tower
                            reply_msg = msg.make_reply()
                            info = StationInfo(plane_id, req_action, closest_runway_id, closest_runway_coords, closest_station_coords, closest_station_dist)
                            reply_msg.body = jsonpickle.encode(info)
                            reply_msg.set_metadata("performative", "confirm_landing")
                            await self.send(reply_msg)    

                        # If no station available
                        else:
                            reply_msg = msg.make_reply()
                            info = RequestDelay(plane_id, req_action, 'No Station Available')
                            reply_msg.body = jsonpickle.encode(info)
                            reply_msg.set_metadata("performative", "delay")
                            await self.send(reply_msg)

                    # If TAKEOFF just use closest runway
                    else:
                        # Notify Control Tower
                        reply_msg = msg.make_reply()
                        info = StationInfo(plane_id, req_action, closest_runway_id, closest_runway_coords, curr_coords, closest_runway_dist)
                        reply_msg.body = jsonpickle.encode(info)
                        reply_msg.set_metadata("performative", "confirm_takeoff")
                        await self.send(reply_msg)          

                # If no runway available
                else:
                    reply_msg = msg.make_reply()
                    info = RequestDelay(plane_id, req_action, 'No Runway Available')
                    reply_msg.body = jsonpickle.encode(info)
                    reply_msg.set_metadata("performative", "delay")
                    await self.send(reply_msg)

# Returns closest coordinates from list and its distance from the starting point
def get_closest(start, locations):
    min_dist = 999999
    min_coords = None
    
    for loc in locations:
        dist = calc_dist(start, loc)
        if dist < min_dist:
            min_dist = dist
            min_coords = loc

    return (min_coords, math.ceil(min_dist))

# Returns distance between two coordinates
def calc_dist(origin, dest):
    return math.sqrt( ((origin[0] - dest[0])**2) + ((origin[1] - dest[1])**2) )