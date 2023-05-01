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

                # Notify Dashboard
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = msg.body
                dashboard_msg.set_metadata("performative", performative)
                await self.send(dashboard_msg)
                
                # Wait out move to runway
                # Free station + occupy runway (notify station manager)
                # Wait out takeoff
                # Free runway (notify station manager)
                # Update Plane State (notify plane)