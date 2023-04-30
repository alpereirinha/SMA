from spade.behaviour import OneShotBehaviour
from spade.message import Message
from messages.planeRequest import PlaneRequest
from classes.enums import *
import jsonpickle
import time

class sendPlaneReqBehav(OneShotBehaviour):

    async def on_start(self):
        self.type = self.get("type")
        self.state = self.get("state")
    
    async def run(self):
        msg = Message(to=self.get("controlTower_jid"))

        if self.state == PlaneState.FLYING:
            req_action = Action.LANDING
        else:
            req_action = Action.TAKEOFF

        req = PlaneRequest(self.agent.jid, self.type, req_action)

        msg.body = jsonpickle.encode(req)
        msg.set_metadata("performative", "request")
        await self.send(msg)

        # If flying, await confirmation. Timeout and try another airport if none after a minute.
        if self.state == PlaneState.FLYING:
            msg = await self.receive(timeout=60)
            if msg and msg.get_metadata("performative") == "confirm": 
                pass
                # TODO - takeoff again after a time
            else:
                cancel_msg = Message(to=self.get("controlTower_jid"))
                cancel_msg.set_metadata("performative", "cancel_request")
                await self.send(cancel_msg)
