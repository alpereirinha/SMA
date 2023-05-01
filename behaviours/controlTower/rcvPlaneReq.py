from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio

class rcvPlaneReqBehav(CyclicBehaviour):
    
    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")
            
            ## Received valid landing/takeoff request
            if performative == "request":

                ## Wait time between requests to avoid conflicts
                await asyncio.sleep(0.5)

                ## Notify Dashboard
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = msg.body
                dashboard_msg.set_metadata("performative", "plane_request")
                await self.send(dashboard_msg)
                
                ## Request info from Station Manager
                station_msg = Message(to=self.get("stationManager_jid"))
                station_msg.body = msg.body
                station_msg.set_metadata("performative", "request")
                await self.send(station_msg)

            ## Received cancellation of LANDING request
            elif performative == "cancel_request":
                
                ## Notify Dashboard
                dashboard_msg = Message(to=self.get("dashboard_jid"))
                dashboard_msg.body = msg.body
                dashboard_msg.set_metadata("performative", "cancel_plane_request")
                await self.send(dashboard_msg)