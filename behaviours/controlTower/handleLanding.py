from spade.behaviour import CyclicBehaviour
from spade.message import Message
from messages.stationUpdate import StationUpdate
import jsonpickle
import asyncio

class handleLandingBehav(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")
            
            ## Process LANDING
            if performative == "confirm_landing":
                msg_data = jsonpickle.decode(msg.body)
                plane_id = str(msg_data.getPlaneId())

                # Remove request from queue
                if self.get("multi_mode"):
                    self.agent.multi_queue.pop(0)
                else:
                    self.agent.landing_queue.pop(0)

                # Confirm landing (notify dashboard)
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

                # Occupy station (notify station manager)
                station_msg = Message(to=self.get("stationManager_jid"))
                info = StationUpdate(plane_id, msg_data.getStationCoords())
                station_msg.body = jsonpickle.encode(info)
                station_msg.set_metadata("performative", "update_station")
                await self.send(station_msg)

                # Update max_landing_queue (one less free space)
                self.set("max_landing_queue", self.get("max_landing_queue") - 1)

                # Wait out landing (notify dashboard)
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = plane_id
                dashboard_msg.set_metadata("performative", "start_action")
                await self.send(dashboard_msg)
                await asyncio.sleep(10)

                # Wait out moving from runway to station (notify dashboard)
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = plane_id
                dashboard_msg.set_metadata("performative", "next_action")
                await self.send(dashboard_msg)
                await asyncio.sleep(msg_data.getDistance()/2)

                # Free runway (notify station manager)
                station_msg = Message(to=self.get("stationManager_jid"))
                info = StationUpdate('', msg_data.getRunwayCoords())
                station_msg.body = jsonpickle.encode(info)
                station_msg.set_metadata("performative", "update_runway")
                await self.send(station_msg)

                # Update Plane State (notify plane)
                plane_msg = Message(to=msg_data.getPlaneId())
                plane_msg.body = str(msg_data.getStationCoords())
                plane_msg.set_metadata("performative", "update")
                await self.send(plane_msg)

                # Landing concluded (notify dashboard)
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = plane_id
                dashboard_msg.set_metadata("performative", "end_action")
                await self.send(dashboard_msg)
