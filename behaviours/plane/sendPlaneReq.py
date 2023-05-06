from spade.behaviour import OneShotBehaviour
from spade.message import Message
from messages.planeRequestFull import PlaneRequestFull
from classes.enums import Action, PlaneState
import jsonpickle

class sendPlaneReqBehav(OneShotBehaviour):

    async def on_start(self):
        self.type = self.get("type")
        self.state = self.get("state")
        self.coordinates = self.get("coordinates")
        self.company = self.get("company")
        self.origin = self.get("origin")
        self.destination = self.get("destination")
    
    async def run(self):
        msg = Message(to=self.get("controlTower_jid"))

        if self.state == PlaneState.FLYING:
            req_action = Action.LANDING
        else:
            req_action = Action.TAKEOFF

        req = PlaneRequestFull(self.agent.jid, self.type, self.coordinates, req_action, self.company, self.origin, self.destination)

        msg.body = jsonpickle.encode(req)
        msg.set_metadata("performative", "request")
        await self.send(msg)

        # If flying, await some response. Timeout and try another airport if no response after a minute.
        if self.state == PlaneState.FLYING:
            response = await self.receive(timeout=60)

            if not response:
                cancel_msg = Message(to=self.get("controlTower_jid"))
                cancel_msg.body = str(self.agent.jid)
                cancel_msg.set_metadata("performative", "cancel_request")
                await self.send(cancel_msg)
                await self.agent.stop()