from spade.behaviour import CyclicBehaviour
from spade.message import Message
from messages.stationUpdate import StationUpdate
from classes.enums import Action
import jsonpickle
import asyncio

class handleTakeoffBehav(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")
            
            ## Process TAKEOFF
            if performative == "confirm_takeoff":
                msg_data = jsonpickle.decode(msg.body)
                plane_id = str(msg_data.getPlaneId())

                # Confirm takeoff (notify dashboard)
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = msg.body
                dashboard_msg.set_metadata("performative", "confirm")
                await self.send(dashboard_msg)

                # Occupy runway (notify station manager)
                station_msg = Message(to=self.get("stationManager_jid"))
                info = StationUpdate(plane_id, msg_data.getRunwayCoords())
                station_msg.body = jsonpickle.encode(info)
                station_msg.set_metadata("performative", "update_runway")
                await self.send(station_msg)

                # Wait out moving from station to runway (notify dashboard)
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = plane_id
                dashboard_msg.set_metadata("performative", "start_action")
                await self.send(dashboard_msg)
                await asyncio.sleep(msg_data.getDistance()/2)

                # Free station (notify station manager)
                station_msg = Message(to=self.get("stationManager_jid"))
                info = StationUpdate('', msg_data.getStationCoords())
                station_msg.body = jsonpickle.encode(info)
                station_msg.set_metadata("performative", "update_station")
                await self.send(station_msg)

                # Wait out takeoff (notify dashboard)
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = plane_id
                dashboard_msg.set_metadata("performative", "next_action")
                await self.send(dashboard_msg)
                await asyncio.sleep(10)

                # Free runway (notify station manager)
                station_msg = Message(to=self.get("stationManager_jid"))
                info = StationUpdate('', msg_data.getRunwayCoords())
                station_msg.body = jsonpickle.encode(info)
                station_msg.set_metadata("performative", "update_runway")
                await self.send(station_msg)

                # Update Plane State (notify plane)
                plane_msg = Message(to=msg_data.getPlaneId())
                plane_msg.body = str(msg_data.getRunwayCoords())
                plane_msg.set_metadata("performative", "update")
                await self.send(plane_msg)

                # Takeoff concluded (notify dashboard)
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = plane_id
                dashboard_msg.set_metadata("performative", "end_action")
                await self.send(dashboard_msg)
