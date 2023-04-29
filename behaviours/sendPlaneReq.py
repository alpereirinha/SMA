from spade.behaviour import OneShotBehaviour
from spade.message import Message
from messages.planeRequest import PlaneRequest
import jsonpickle
import time

FLYING = 0
LANDED = 1

LANDING = 0
TAKEOFF = 1

class sendPlaneReqBehav(OneShotBehaviour):

    async def on_start(self):
        self.type = self.get("type")
        self.state = self.get("state")
    
    async def run(self):
        msg = Message(to=self.get("controlTower_jid"))
        req = PlaneRequest(self.agent.jid, self.type, self.state) # FLYING -> LANDING; LANDED -> TAKEOFF;
        msg.body = jsonpickle.encode(req)
        msg.set_metadata("performative", "request")
        await self.send(msg)

        # If flying, await confirmation. Timeout and try another airport if none after a minute.
        if self.state == FLYING:
            msg = await self.receive(timeout=60)
            if msg: 
                pass
                # takeoff again after x time TODO
            else:
                cancel_msg = Message(to=self.get("controlTower_jid"))
                cancel_msg.set_metadata("performative", "cancel_request")
                await self.send(cancel_msg)
