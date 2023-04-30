from spade.behaviour import CyclicBehaviour
from spade.message import Message
from messages.stationUpdate import stationUpdate
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

                # Notify Dashboard
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = msg.body
                dashboard_msg.set_metadata("performative", performative)
                await self.send(dashboard_msg)

                # Confirm landing (notify plane)
                plane_msg = Message(to=msg_data.getPlaneId())
                plane_msg.set_metadata("performative", "confirm")
                await self.send(plane_msg)

                # Occupy runway (notify station manager)
                station_msg = Message(to=self.get("stationManager_jid"))
                info = stationUpdate(plane_id, msg_data.getRunwayCoords())
                station_msg.body = jsonpickle.encode(info)
                station_msg.set_metadata("performative", "update_runway")
                await self.send(station_msg)

                # Wait out landing - TODO dashboard
                print(f'{plane_id} began landing...')
                await asyncio.sleep(10)
                print(f'{plane_id} finished landing. Moving to station at {msg_data.getStationCoords()}.')

                # Wait out parking in station - TODO dashboard
                await asyncio.sleep(msg_data.getDistance())
                print(f'{plane_id} finished parking.')

                # Occupy station (notify station manager)
                station_msg = Message(to=self.get("stationManager_jid"))
                info = stationUpdate(plane_id, msg_data.getStationCoords())
                station_msg.body = jsonpickle.encode(info)
                station_msg.set_metadata("performative", "update_station")
                await self.send(station_msg)

                # Free runway (notify station manager)
                station_msg = Message(to=self.get("stationManager_jid"))
                info = stationUpdate('', msg_data.getRunwayCoords())
                station_msg.body = jsonpickle.encode(info)
                station_msg.set_metadata("performative", "update_runway")
                await self.send(station_msg)

                # Update Plane State (notify plane)
                plane_msg = Message(to=msg_data.getPlaneId())
                plane_msg.set_metadata("performative", "update")
                await self.send(plane_msg)