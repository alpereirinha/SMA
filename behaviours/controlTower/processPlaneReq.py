from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import jsonpickle

class processPlaneReqBehav(CyclicBehaviour):
  
    async def run(self):
        for req in self.get("queue"):

            # Request info from Station Manager
            station_msg = Message(to=self.get("stationManager_jid"))
            station_msg.body = jsonpickle.encode(req)
            station_msg.set_metadata("performative", "request")
            await self.send(station_msg)

            # Wait time between requests to avoid conflicts
            await asyncio.sleep(1)
