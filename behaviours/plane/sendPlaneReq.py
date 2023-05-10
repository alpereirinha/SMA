from spade.behaviour import OneShotBehaviour
from spade.message import Message
from messages.planeRequestFull import PlaneRequestFull
from messages.requestIssue import RequestIssue
from classes.enums import Action, PlaneState
import jsonpickle

class sendPlaneReqBehav(OneShotBehaviour):

    async def cancelRequest(self, issue):
        cancel_msg = Message(to=self.get("controlTower_jid"))
        info = RequestIssue(str(self.agent.jid), Action.LANDING, issue)
        cancel_msg.body = jsonpickle.encode(info)
        cancel_msg.set_metadata("performative", "cancel_request")
        await self.send(cancel_msg)
        await self.agent.stop()

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

        # If flying, await some response 
        if self.state == PlaneState.FLYING:
            response = await self.receive(timeout=60)

            # Timeout and try another airport if no response after a minute
            if not response:
                await self.cancelRequest("No Response")

            # Timeout and try another airport if still on queue after 2 minutes
            else:
                if response.get_metadata("performative") == "ok":
                    msg = await self.receive(timeout=120)
                    if not msg:
                        await self.cancelRequest("Timed out")