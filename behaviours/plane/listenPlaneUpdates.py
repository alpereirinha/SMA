from spade.behaviour import CyclicBehaviour
from spade.message import Message
from messages.planeRequestFull import PlaneRequestFull
from classes.enums import Action, PlaneState
import jsonpickle
import asyncio

class listenPlaneUpdatesBehav(CyclicBehaviour):

    async def on_start(self):
        self.type = self.get("type")
        self.company = self.get("company")
        self.origin = self.get("origin")
        self.destination = self.get("destination")

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            if performative == "update":
                self.set("coordinates", eval(msg.body))

                if self.get("state") == PlaneState.LANDED:
                    self.set("state", PlaneState.FLYING)
                    await self.agent.stop() # Leave the system after flying off
                else:
                    self.set("state", PlaneState.LANDED)

                    # Request TAKEOFF again 30 sec after landing
                    await asyncio.sleep(30)
                    new_msg = Message(to=self.get("controlTower_jid"))
                    new_req = PlaneRequestFull(self.agent.jid, self.type, self.get("coordinates"), Action.TAKEOFF, self.company, self.origin, self.destination)
                    new_msg.body = jsonpickle.encode(new_req)
                    new_msg.set_metadata("performative", "request")
                    await self.send(new_msg)

            elif performative == "refused":
                await self.agent.stop() # Leave the system (try another airport)