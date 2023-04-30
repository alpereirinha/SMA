from spade.behaviour import CyclicBehaviour
from spade.message import Message
from messages.planeRequest import PlaneRequest
from messages.stationInfo import StationInfo
from classes.enums import *
import math
import jsonpickle

class rcvStationInfoReqBehav(CyclicBehaviour):

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
                for r in self.runways:
                    if (r.action_type == req_action or r.action_type == Action.MULTI) and not r.plane:
                        available_runways.append(r)

                # If runway available
                if len(available_runways) > 0 :

                    # If LANDING check for closest compatible station
                    if req_action == Action.LANDING:
                        plane_type = msg_data.getPlaneType()
                        available_stations = []

                        # Check stations
                        for s in self.stations:
                            if s.type == plane_type and not s.plane:
                                available_stations.append(s)

                        # If station available
                        if len(available_stations) > 0 :
                            
                            # Pick first available runway, check distance to available stations
                            station_dist = get_closest_dist(available_runways[0], available_stations)

                            # Notify Control Tower
                            reply_msg = msg.make_reply()
                            info = StationInfo(plane_id, req_action, 100, station_dist)
                            reply_msg.body = jsonpickle.encode(info)
                            reply_msg.set_metadata("performative", "confirm")
                            await self.send(reply_msg)    

                        # If no station available
                        else:
                            reply_msg = msg.make_reply()
                            reply_msg.body = plane_id
                            reply_msg.set_metadata("performative", "delay")
                            await self.send(reply_msg)

                    # If TAKEOFF check for closest runway
                    else:
                        runway_dist = 0
                        for s in self.stations:
                            # Find current station
                            if s.plane == plane_id:
                                # Check distance to available runways
                                runway_dist = get_closest_dist(s, available_runways)
                                break

                        # Notify Control Tower
                        reply_msg = msg.make_reply()
                        info = StationInfo(plane_id, req_action, runway_dist, 0)
                        reply_msg.body = jsonpickle.encode(info)
                        reply_msg.set_metadata("performative", "confirm")
                        await self.send(reply_msg)          

                # If no available runway
                else:
                    reply_msg = msg.make_reply()
                    reply_msg.body = plane_id
                    reply_msg.set_metadata("performative", "delay")
                    await self.send(reply_msg)

        ## Time out       
        else:
            pass


def get_closest_dist(start, locations):
    min_dist = 999999
    
    for loc in locations:
        dist = calc_dist(start.coordinates, loc.coordinates)
        if dist < min_dist:
            min_dist = dist

    return math.ceil(min_dist)

def calc_dist(origin, dest):
    return math.sqrt( ((origin[0] - dest[0])**2) + ((origin[1] - dest[1])**2) )