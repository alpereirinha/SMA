from spade.behaviour import CyclicBehaviour
from spade.message import Message
from messages.planeRequest import PlaneRequest
from messages.stationInfo import StationInfo
import jsonpickle

LANDING = 0
TAKEOFF = 1
MULTI = 2

SHIPPING = 0
PASSENGERS = 1

FREE = 0
OCCUPIED = 1

class handleStationInfoReqBehav(CyclicBehaviour):

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
                request_type = msg_data.getRequestType()
                
                # Check runways
                available_runways = []
                for r in self.runways:
                    if (r.type == request_type or r.type == MULTI) and r.state == FREE:
                        available_runways.append(r)

                # If runway available
                if len(available_runways) > 0 :

                    # If LANDING check for closest compatible station
                    if request_type == LANDING:
                        plane_type = msg_data.getPlaneType()
                        available_stations = []

                        # Check stations
                        for s in self.stations:
                            if s.type == plane_type and s.state == FREE:
                                available_stations.append(s)

                        # If station available
                        if len(available_stations) > 0 :
                            # TODO - check distances between available stations and runways
                            runway_dist = 12
                            station_dist = 12

                            reply_msg = msg.make_reply()
                            info = StationInfo(msg_data.getPlaneJid(), runway_dist, station_dist)
                            reply_msg.body = jsonpickle.encode(info)
                            reply_msg.set_metadata("performative", "confirm")
                            await self.send(reply_msg)    

                        # If no station available
                        else:
                            reply_msg = msg.make_reply()
                            reply_msg.body = str(msg_data.getPlaneJid())
                            reply_msg.set_metadata("performative", "delay")
                            await self.send(reply_msg)

                    # If TAKEOFF check for closest runway
                    else:
                        # TODO - find current station, check distance to available runways
                        runway_dist = 12

                        reply_msg = msg.make_reply()
                        info = StationInfo(msg_data.getPlaneJid(), runway_dist, 0)
                        reply_msg.body = jsonpickle.encode(info)
                        reply_msg.set_metadata("performative", "confirm")
                        await self.send(reply_msg)          

                # If no available runway
                else:
                    reply_msg = msg.make_reply()
                    reply_msg.body = str(msg_data.getPlaneJid())
                    reply_msg.set_metadata("performative", "delay")
                    await self.send(reply_msg)

        ## Time out       
        else:
            pass