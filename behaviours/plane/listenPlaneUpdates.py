from spade.behaviour import CyclicBehaviour
from spade.message import Message
from messages.planeRequestFull import PlaneRequestFull
from classes.enums import *
import jsonpickle
import asyncio

class listenPlaneUpdatesBehav(CyclicBehaviour):

    async def on_start(self):
        self.type = self.get("type")
        self.state = self.get("state")
        self.company = self.get("company")
        self.origin = self.get("origin")
        self.destination = self.get("destination")

    async def run(self):
        msg = await self.receive(timeout=30)

        if msg:
            performative = msg.get_metadata("performative")

            if performative == "update":
                if self.state == PlaneState.LANDED:
                    self.state = PlaneState.FLYING
                else:
                    self.state = PlaneState.LANDED

                    # Request TAKEOFF again 30 sec after landing
                    await asyncio.sleep(30)
                    new_msg = Message(to=self.get("controlTower_jid"))
                    new_req = PlaneRequestFull(self.agent.jid, self.type, Action.TAKEOFF, self.company, self.origin, self.destination)
                    new_msg.body = jsonpickle.encode(new_req)
                    new_msg.set_metadata("performative", "request")
                    await self.send(new_msg)