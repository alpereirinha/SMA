from spade.behaviour import CyclicBehaviour
from spade.message import Message
from messages.stationUpdate import stationUpdate
from classes.enums import *
import jsonpickle
import asyncio

class rcvStationInfoBehav(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            if performative == "confirm":
                msg_data = jsonpickle.decode(msg.body)
                req_action = msg_data.getRequestAction()
                plane_id = str(msg_data.getPlaneId())

                # Notify Dashboard
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = msg.body
                dashboard_msg.set_metadata("performative", "plane_request_reply")
                await self.send(dashboard_msg)

                # Handle LANDING
                if req_action == Action.LANDING:

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

                    # Wait out landing - TODO
                    #print(f'{plane_id} began landing...')
                    #await asyncio.sleep(10)
                    #print(f'{plane_id} finished landing. Moving to station at {msg_data.getStationCoords()}.')
                    
                    # Wait out parking in station - TODO
                    #await asyncio.sleep(msg_data.getDistance())
                    #print(f'{plane_id} finished parking.')

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
                    # TODO ...

                # Handle TAKEOFF
                else:
                    pass
                    # Wait out move to runway
                    # Free station + occupy runway (notify station manager)
                    # Wait out takeoff
                    # Free runway (notify station manager)
                    # Update Plane State (notify plane)

            elif performative == "delay":
                # Notify Dashboard
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = msg.body
                dashboard_msg.set_metadata("performative", "plane_request_reply")
                await self.send(dashboard_msg)

                # TODO - queue handling, notify plane, cancel if queue is full
            
        else:
            pass