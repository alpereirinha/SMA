from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import jsonpickle

class processQueueLandingBehav(CyclicBehaviour):
  
    async def run(self):
        
        # Check first plane in LANDING queue
        if len(self.agent.landing_queue):

            # Request info from Station Manager
            station_msg = Message(to=self.get("stationManager_jid"))
            station_msg.body = jsonpickle.encode(self.agent.landing_queue[0])
            station_msg.set_metadata("performative", "request")
            await self.send(station_msg)

            # Wait time between requests to avoid conflicts
            await asyncio.sleep(1)